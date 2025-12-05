from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    text: str = Field(..., description="News article text to analyze", min_length=10)
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Breaking news: Scientists have discovered a new planet in our solar system."
            }
        }

class PredictionResponse(BaseModel):
    text: str = Field(..., description="Original input text")
    prediction: str = Field(..., description="Predicted label (e.g., fake, real)")
    confidence: float = Field(..., description="Confidence score for the prediction", ge=0, le=1)
    probabilities: dict[str, float] = Field(..., description="Probabilities for all labels")
    is_fake: bool = Field(..., description="Whether the news is considered fake")
    classification_type: str = Field(default="binary", description="Type of classification (binary or multi-class)")
    
    # News validation fields
    news_validation: dict | None = Field(default=None, description="News source validation results")
    news_insight: str | None = Field(default=None, description="Insight from news validation")
    verification_boost: float | None = Field(default=None, description="Confidence adjustment from news validation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Breaking news: Scientists have discovered a new planet in our solar system.",
                "prediction": "fake",
                "confidence": 0.85,
                "probabilities": {
                    "real": 0.15,
                    "fake": 0.85
                },
                "is_fake": True,
                "classification_type": "binary",
                "news_validation": {
                    "verification_status": "not_found",
                    "total_articles_found": 0
                },
                "news_insight": "No news coverage found"
            }
        }
