from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

class SuggestionService:
    def __init__(self):
        # Load model embedding
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        
        # Định nghĩa các template câu hỏi theo chủ đề
        self.topic_templates = {
            "experience": [
                "Kinh nghiệm làm việc với {topic}?",
                "Dự án {topic} khó khăn nhất?",
                "Bài học từ dự án {topic}?"
            ],
            "technical": [
                "Công nghệ nào được dùng trong {topic}?",
                "Architecture của {topic} như thế nào?",
                "Challenges kỹ thuật khi làm {topic}?"
            ],
            "career": [
                "Con đường sự nghiệp trong {topic}?",
                "Kỹ năng cần có để làm {topic}?",
                "Lời khuyên cho người mới bắt đầu {topic}?"
            ]
        }
        
        # Các topic chính từ CV
        self.main_topics = [
            "AI", "Machine Learning", "Deep Learning",
            "Computer Vision", "NLP", "Data Science"
        ]
        
    def get_suggestions(self, 
                       current_message: str,
                       chat_history: List[str],
                       n_suggestions: int = 3) -> List[str]:
        try:
            # Tạo embedding cho tin nhắn hiện tại
            message_embedding = self.model.encode(current_message)
            
            # Tạo embedding cho các topic
            topic_embeddings = self.model.encode(self.main_topics)
            
            # Tính similarity
            similarities = np.dot(topic_embeddings, message_embedding)
            
            # Lấy top topics liên quan nhất
            top_topic_indices = np.argsort(similarities)[-2:]
            relevant_topics = [self.main_topics[i] for i in top_topic_indices]
            
            # Tạo suggestions dựa trên topics
            suggestions = []
            for topic in relevant_topics:
                for template_type in self.topic_templates.values():
                    suggestions.extend([
                        template.format(topic=topic)
                        for template in template_type
                    ])
            
            # Thêm một số câu hỏi chung
            general_questions = [
                "Có thể chia sẻ thêm về điều này không?",
                "Ví dụ cụ thể về vấn đề này?",
                "Còn khía cạnh nào khác của vấn đề này?"
            ]
            suggestions.extend(general_questions)
            
            # Chọn ngẫu nhiên n_suggestions
            if len(suggestions) > n_suggestions:
                suggestions = np.random.choice(
                    suggestions, 
                    size=n_suggestions, 
                    replace=False
                ).tolist()
            
            return suggestions
            
        except Exception as e:
            print(f"Error generating suggestions: {str(e)}")
            return ["Có thể chia sẻ thêm không?",
                   "Ví dụ cụ thể?",
                   "Điều này áp dụng như thế nào?"]