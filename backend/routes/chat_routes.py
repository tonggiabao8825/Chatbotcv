from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ai_service import DeepSeekService
from services.suggestion_service import SuggestionService
from utils.cv_loader import load_cv
from utils.text_processor import clean_response
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
ai_service = DeepSeekService()
suggestion_service = SuggestionService()

class ChatRequest(BaseModel):
    user_message: str

@router.post("/query")
def chat_with_ai(request: ChatRequest):
    try:
        # Tải CV
        cv_content = load_cv()
        
        # Tạo prompt với context từ CV
        prompt = f"Dựa trên CV sau đây, hãy trả lời câu hỏi: {request.user_message}\n\nCV:\n{cv_content}"
        
        # Gọi AI service
        logger.info("Prompt: " + prompt)
        response = ai_service.generate_response(prompt)
        
        # Xử lý response để loại bỏ phần thinking
        cleaned_response = clean_response(response)
        
        logger.info(cleaned_response)
        # Tạo gợi ý câu hỏi tiếp theo
        related_questions = suggestion_service.get_suggestions(request.user_message, [])
        
        return {
            "answer": cleaned_response,
            "related_questions": related_questions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
