import os
from dotenv import load_dotenv
import openai
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class DeepSeekService:
    def __init__(self):
        # Khởi tạo OpenAI client với Azure config
        self.client = openai.OpenAI(
            api_key=os.getenv("AZURE_API_KEY"),
            base_url="https://DeepSeek-R1-xacdm.eastus.models.ai.azure.com"
        )
        self.model = "deepseek-chat"

    def generate_response(self, prompt: str) -> str:
        try:
            logger.info("Sending request to DeepSeek API")
            messages = [
                {"role": "system", "content": "You are an AI assistant with expertise in AI, Machine Learning, and Software Development. Answer questions based on the provided CV context. DO NOT include any thinking process or notes to yourself in your response. Provide direct, concise answers only."},
                {"role": "user", "content": prompt}
            ]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )

            # Lấy response content
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error calling DeepSeek API: {str(e)}")
            raise Exception(str(e))


deepseek_service = DeepSeekService()

def call_openai_api(prompt: str) -> str:
    return deepseek_service.generate_response(prompt)

def call_claude_api(prompt: str) -> str:
    return deepseek_service.generate_response(prompt)
