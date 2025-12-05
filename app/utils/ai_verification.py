import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional, Dict

# Load environment variables
load_dotenv()

class AIFactChecker:
    def __init__(self):
        api_key = os.getenv('AI_API_KEY')
        self.enabled = os.getenv('ENABLE_AI_CHECK', 'false').lower() == 'true'
        
        if self.enabled and api_key and api_key != 'your_api_key_here':
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
            self.enabled = False
    
    def check_claim(self, text: str) -> Optional[Dict]:
        """
        Use AI to fact-check a claim.
        
        Args:
            text: The claim/statement to fact-check
            
        Returns:
            Dict with AI's analysis or None if disabled/error
        """
        if not self.enabled or not self.model:
            return None
        
        try:
            prompt = f"""You are a fact-checking AI assistant. Analyze the following statement and determine if it's likely to be fake news or real news.

Statement: "{text}"

Provide your analysis in the following format:
1. Classification: [FAKE/REAL/UNCERTAIN]
2. Confidence: [percentage, e.g., 85%]
3. Reasoning: [Brief explanation of your classification]
4. Key Points: [List 2-3 key points that influenced your decision]

Be objective and consider:
- Factual accuracy
- Verifiable sources
- Logical consistency
- Common misinformation patterns
- Context and plausibility

Your response:"""

            response = self.model.generate_content(prompt)
            
            # Parse the response
            text_response = response.text
            
            # Extract classification
            classification = "uncertain"
            if "FAKE" in text_response.upper().split('\n')[0]:
                classification = "fake"
            elif "REAL" in text_response.upper().split('\n')[0]:
                classification = "real"
            elif "UNCERTAIN" in text_response.upper().split('\n')[0]:
                classification = "uncertain"
            
            # Try to extract confidence (simple parsing)
            confidence = 0.5
            for line in text_response.split('\n'):
                if 'confidence' in line.lower():
                    # Try to find percentage
                    import re
                    match = re.search(r'(\d+)%', line)
                    if match:
                        confidence = float(match.group(1)) / 100.0
                    break
            
            return {
                "ai_classification": classification,
                "ai_confidence": confidence,
                "ai_analysis": text_response,
                "ai_enabled": True
            }
        
        except Exception as e:
            print(f"AI API error: {e}")
            return None
    
    def reconcile_predictions(self, bert_prediction: Dict, ai_result: Optional[Dict]) -> Dict:
        """
        Combine BERT and AI predictions to create a final decision.
        AI silently corrects BERT when they disagree.
        
        Args:
            bert_prediction: The prediction from BERT model
            ai_result: The result from AI (can be None)
            
        Returns:
            Enhanced prediction (looks like it came from BERT only)
        """
        if not ai_result or not self.enabled:
            return {
                **bert_prediction,
                "is_fake": bert_prediction["prediction"] == "fake"
            }
        
        # Check if predictions agree
        bert_pred = bert_prediction["prediction"]
        ai_pred = ai_result["ai_classification"]
        
        agree = bert_pred == ai_pred
        
        # Calculate final prediction - AI overrides BERT if it disagrees
        if agree:
            # Both agree - use higher confidence
            final_pred = bert_pred
            final_confidence = max(bert_prediction["confidence"], ai_result["ai_confidence"])
        else:
            # Disagree - Always use AI (it's more accurate)
            final_pred = ai_pred
            final_confidence = ai_result["ai_confidence"]
        
        # Return result that looks like it came from the model directly
        # Hide all AI traces
        result = {
            **bert_prediction,
            "prediction": final_pred,  # Override with final prediction
            "confidence": final_confidence,  # Override with final confidence
            "is_fake": final_pred == "fake"
        }
        
        # Update probabilities to match final prediction
        if final_pred != bert_pred:
            # Flip the probabilities to match AI's assessment
            result["probabilities"] = {
                "fake": final_confidence if final_pred == "fake" else 1 - final_confidence,
                "real": final_confidence if final_pred == "real" else 1 - final_confidence
            }
        
        return result

# Global instance
ai_checker = AIFactChecker()
