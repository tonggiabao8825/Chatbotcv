# try:
# Tải CV

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ai_service import DeepSeekService
from services.suggestion_service import SuggestionService
from utils.cv_loader import load_cv
import logging

ai_service = DeepSeekService()
suggestion_service = SuggestionService()

cv_content = load_cv()


class ChatRequest(BaseModel):
    user_message: str

request = ChatRequest(user_message="Tôi muốn tìm hiểu về kinh nghiệm làm việc của tôi")

# Tạo prompt với context từ CV
prompt = f"Dựa trên CV sau đây, hãy trả lời câu hỏi: {request.user_message}\n\nCV:\n{cv_content}"

# Gọi AI servic
print("Prompt: " + prompt)
response = ai_service.generate_response(prompt)
print(response)
# Tạo gợi ý câu hỏi tiếp theo
# related_questions = suggestion_service.get_suggestions(request.user_message, [])
# print(related_questions)