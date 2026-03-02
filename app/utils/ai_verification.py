import os
import re
import time
from google import genai
from dotenv import load_dotenv
from typing import Optional, Dict, List

load_dotenv()

# Models to try in order (current stable models per docs.ai.google.dev/gemini-api/docs/models)
_CANDIDATE_MODELS = [
    "gemini-2.5-flash-lite",     # most budget-friendly + fastest, separate quota pool
    "gemini-2.5-flash",          # best price-performance fallback
    "gemini-2.0-flash",          # deprecated but still available as last resort
]

_MAX_RETRIES = 3
_RETRY_DELAY = 30  # seconds to wait on quota error

class AIFactChecker:
    def __init__(self):
        api_key = os.getenv('AI_API_KEY')
        self.enabled = os.getenv('ENABLE_AI_CHECK', 'true').lower() == 'true'
        self._client = None
        self._model_id = None

        if api_key and api_key != 'your_api_key_here' and len(api_key) > 10:
            try:
                # New google-genai SDK uses a Client object
                self._client = genai.Client(api_key=api_key)
                # Pick the first model that doesn't raise on a list call
                self._model_id = _CANDIDATE_MODELS[0]  # will be confirmed on first call
                self.enabled = True
                print(f"✓ Gemini AI (google-genai SDK) ready — primary model: {self._model_id}")
            except Exception as e:
                print(f"⚠ Failed to initialise Gemini AI: {e}")
                self._client = None
                self._model_id = None
                self.enabled = False
        else:
            self._client = None
            self._model_id = None
            self.enabled = False
            print("⚠ AI API key not configured, using BERT model only")

    # ── robust response parser ─────────────────────────────────────────────────
    def _parse_response(self, text_response: str) -> Optional[Dict]:
        """
        Parse Gemini's structured response.
        Uses strict regex to avoid false-fake from lines like 'REAL (not FAKE)'.
        """
        print(f"[Gemini raw response]:\n{text_response}\n---")

        # Strict match: look for CLASSIFICATION line and extract the LAST word
        # which should be exactly REAL or FAKE
        classification = "real"  # default — bias toward real to avoid over-flagging
        for line in text_response.split('\n'):
            if 'CLASSIFICATION' in line.upper():
                # Extract the classification value after the colon
                after_colon = line.split(':', 1)[-1].strip().upper()
                # Check for FAKE strictly — must appear as a standalone word at the end
                # "FAKE" matches, "NOT FAKE" → skip (NOT comes before FAKE)
                # Use word-boundary regex so REAL wins if both appear
                if re.search(r'\bFAKE\b', after_colon) and not re.search(r'\bNOT\s+FAKE\b', after_colon):
                    classification = "fake"
                elif re.search(r'\bREAL\b', after_colon):
                    classification = "real"
                break

        confidence = 0.75
        for line in text_response.split('\n'):
            if 'CONFIDENCE' in line.upper():
                match = re.search(r'(\d+(?:\.\d+)?)', line)
                if match:
                    confidence = float(match.group(1)) / 100.0
                    confidence = min(max(confidence, 0.50), 0.99)
                break

        return {
            "prediction": classification,
            "confidence": confidence,
            "probabilities": {
                "fake": confidence if classification == "fake" else round(1 - confidence, 4),
                "real": confidence if classification == "real" else round(1 - confidence, 4),
            },
            "is_fake": classification == "fake",
            "ai_reasoning": text_response,
            "ai_enabled": True,
        }

    # ── context-aware primary prediction ──────────────────────────────────────
    def predict_with_context(
        self,
        text: str,
        news_articles: Optional[List[Dict]] = None,
    ) -> Optional[Dict]:
        """
        PRIMARY predictor. Gemini receives:
          - The user's claim / headline
          - Real news articles (title + description + fetched body snippet + URL)
        Uses evidence to decide REAL vs FAKE.
        """
        if not self.enabled or not self._client:
            return None

        try:
            # ── Build evidence block ──────────────────────────────────────────
            evidence_block = ""
            usable_articles = [a for a in (news_articles or []) if a.get("title")]
            if usable_articles:  # noqa: SIM102
                lines = []
                for i, art in enumerate(usable_articles[:5], 1):
                    title    = art.get("title", "").strip()
                    source   = art.get("source", "Unknown")
                    url      = art.get("url", "")
                    pub_date = (art.get("published_at") or "").strip()
                    desc     = (art.get("description") or art.get("snippet") or "").strip()[:300]
                    snippet  = (art.get("fetched_snippet") or "").strip()[:500]

                    entry  = f"[Article {i}] {source}\n"
                    if pub_date:
                        entry += f"  Published: {pub_date}\n"
                    entry += f"  Headline : {title}\n"
                    if desc:
                        entry += f"  Summary  : {desc}\n"
                    if snippet:
                        entry += f"  Body text: {snippet}\n"
                    if url:
                        entry += f"  URL      : {url}\n"
                    lines.append(entry)

                evidence_block = (
                    "\n=== LIVE NEWS ARTICLES RETRIEVED FROM THE WEB ===\n"
                    + "\n".join(lines)
                    + "=== END OF RETRIEVED ARTICLES ===\n"
                )

            # ── Prompt ────────────────────────────────────────────────────────
            if evidence_block:
                prompt = f"""You are an expert fact-checker with access to real-time news.

CLAIM TO VERIFY: "{text}"

I searched the web and found these real news articles published recently:
{evidence_block}

INSTRUCTIONS:
1. Compare the claim against the articles above.
2. If multiple credible sources report this (or something very similar) → it is REAL.
3. If the claim contradicts, distorts, or exaggerates what the articles say → it is FAKE.
4. If no retrieved article is directly relevant, rely on your general knowledge.
5. Recent events (2024–2026) may be beyond your training data — in that case trust the retrieved articles entirely.
6. Never mark something FAKE just because it is surprising. Real events can be surprising.

YOU MUST RESPOND IN EXACTLY THIS FORMAT — no preamble, no explanation outside the format:
CLASSIFICATION: REAL
CONFIDENCE: 85%
REASONING: The claim matches reporting from BBC and Reuters which both confirmed this event.

(Replace the example values with your actual assessment.)"""
            else:
                prompt = f"""You are an expert fact-checker.

CLAIM TO VERIFY: "{text}"

No live news articles were found for this claim. Use your general knowledge.

INSTRUCTIONS:
- Default to REAL unless there is clear evidence of misinformation (impossible statistics,
  known hoaxes, logical impossibilities, or patterns of manipulative framing).
- Be especially cautious about marking recent events (2024–2026) as fake since they may
  simply be outside your training cutoff.

YOU MUST RESPOND IN EXACTLY THIS FORMAT — no preamble:
CLASSIFICATION: REAL
CONFIDENCE: 70%
REASONING: Brief explanation here."""

            # ── Call Gemini — try each model, fall to next on quota error ────
            last_error = None
            for attempt in range(_MAX_RETRIES):
                all_quota = True
                for model_id in _CANDIDATE_MODELS:
                    try:
                        response = self._client.models.generate_content(
                            model=model_id,
                            contents=prompt,
                        )
                        self._model_id = model_id
                        result = self._parse_response(response.text)
                        if result:
                            result["context_articles_used"] = len(usable_articles)
                        return result
                    except Exception as model_err:
                        err_str = str(model_err)
                        last_error = model_err
                        is_quota = (
                            "quota" in err_str.lower()
                            or "429" in err_str
                            or "resource_exhausted" in err_str.lower()
                        )
                        if is_quota:
                            # Parse suggested retry delay from error body
                            delay_match = re.search(r'retry in (\d+(?:\.\d+)?)s', err_str.lower())
                            suggested = int(float(delay_match.group(1))) + 2 if delay_match else _RETRY_DELAY
                            print(f"⚠ Quota on {model_id} (attempt {attempt+1}), trying next model…")
                            # DO NOT sleep here — try next model first
                            continue  # ← try next model immediately
                        else:
                            all_quota = False
                            print(f"⚠ Model {model_id} error: {err_str[:120]}")
                            continue  # try next model

                # All models failed this attempt
                if all_quota and attempt < _MAX_RETRIES - 1:
                    wait = suggested if 'suggested' in dir() else _RETRY_DELAY
                    print(f"⚠ All models quota-exhausted. Waiting {wait}s before retry {attempt+2}/{_MAX_RETRIES}…")
                    time.sleep(wait)

            print(f"Gemini: all {len(_CANDIDATE_MODELS)} models failed after {_MAX_RETRIES} attempts. Last error: {str(last_error)[:200]}")
            return None

        except Exception as e:
            print(f"Gemini unexpected error: {e}")
            return None

    # ── backwards-compat wrappers ──────────────────────────────────────────────
    def predict(self, text: str) -> Optional[Dict]:
        return self.predict_with_context(text, news_articles=None)

    def check_claim(self, text: str) -> Optional[Dict]:
        return self.predict(text)

    def reconcile_predictions(self, bert_prediction: Dict, ai_result: Optional[Dict]) -> Dict:
        if ai_result and self.enabled:
            return {
                "text": bert_prediction.get("text", ""),
                "prediction": ai_result["prediction"],
                "confidence": ai_result["confidence"],
                "probabilities": ai_result["probabilities"],
                "is_fake": ai_result["is_fake"],
                "classification_type": "binary",
            }
        return {**bert_prediction, "is_fake": bert_prediction["prediction"] == "fake"}


# Global instance
ai_checker = AIFactChecker()

