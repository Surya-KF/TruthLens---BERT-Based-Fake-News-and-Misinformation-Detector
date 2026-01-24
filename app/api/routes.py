from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.models.bert_model import get_model, predict_fake_news
from app.utils.ai_verification import ai_checker
from app.utils.news_validator import news_validator
from app.auth import get_current_user
from app.database import get_predictions_collection

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict(
    request: PredictionRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Predict whether a news article is fake or real.
    Uses Gemini AI as primary predictor, with BERT as fallback.
    Requires authentication.
    
    Args:
        request: PredictionRequest containing the news text
        
    Returns:
        PredictionResponse with prediction label, confidence, and probabilities
    """
    try:
        # Try AI prediction first (primary)
        ai_result = ai_checker.predict(request.text)
        
        if ai_result:
            # AI prediction successful - use it
            final_result = ai_result
            final_result["text"] = request.text
        else:
            # Fallback to BERT model
            model, tokenizer, checkpoint = get_model()
            bert_result = predict_fake_news(request.text, model, tokenizer, checkpoint)
            final_result = {
                **bert_result,
                "is_fake": bert_result["prediction"] == "fake"
            }
        
        # Validate against real news sources
        news_validation = news_validator.validate_claim(request.text)
        
        # Add news validation insights
        final_result = news_validator.enhance_prediction(final_result, ai_result, news_validation)
        
        # Save prediction to history
        predictions_collection = get_predictions_collection()
        prediction_record = {
            "user_id": str(current_user["_id"]),
            "text": request.text[:500],  # Limit stored text
            "prediction": final_result["prediction"],
            "confidence": final_result["confidence"],
            "is_fake": final_result["is_fake"],
            "created_at": datetime.utcnow()
        }
        await predictions_collection.insert_one(prediction_record)
        
        return final_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.post("/batch-predict")
async def batch_predict(
    texts: list[str],
    current_user: dict = Depends(get_current_user)
):
    """
    Predict multiple news articles at once.
    Uses Gemini AI as primary predictor, with BERT as fallback.
    Requires authentication.
    
    Args:
        texts: List of news article texts
        
    Returns:
        List of predictions
    """
    try:
        model, tokenizer, checkpoint = get_model()
        results = []
        predictions_collection = get_predictions_collection()
        
        for text in texts:
            # Try AI prediction first (primary)
            ai_result = ai_checker.predict(text)
            
            if ai_result:
                final_result = ai_result
                final_result["text"] = text
            else:
                # Fallback to BERT
                bert_result = predict_fake_news(text, model, tokenizer, checkpoint)
                final_result = {
                    **bert_result,
                    "is_fake": bert_result["prediction"] == "fake"
                }
            
            # Validate against news sources
            news_validation = news_validator.validate_claim(text)
            final_result = news_validator.enhance_prediction(final_result, ai_result, news_validation)
            results.append(final_result)
            
            # Save to history
            prediction_record = {
                "user_id": str(current_user["_id"]),
                "text": text[:500],
                "prediction": final_result["prediction"],
                "confidence": final_result["confidence"],
                "is_fake": final_result["is_fake"],
                "created_at": datetime.utcnow()
            }
            await predictions_collection.insert_one(prediction_record)
        
        return {"predictions": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")
