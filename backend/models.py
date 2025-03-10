from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    user_message: str
    model: Optional[str] = "deepseek"  # Default to deepseek
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7
