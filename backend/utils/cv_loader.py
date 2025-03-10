import os
from pathlib import Path

def load_cv() -> str:
    """
    Load CV content from file
    """
    try:
        # Sử dụng Path để xử lý đường dẫn cross-platform
        cv_path = Path(__file__).parent.parent / 'data' / 'cv.txt'
        
        if not cv_path.exists():
            raise FileNotFoundError(f"CV file not found at {cv_path}")
        
        with open(cv_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        return content
    except Exception as e:
        raise Exception(f"Error loading CV: {str(e)}")
