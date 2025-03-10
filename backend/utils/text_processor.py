def clean_response(text: str) -> str:
    """
    Xử lý response để loại bỏ các phần không cần thiết
    """
    # Loại bỏ phần thinking
    if "<think>" in text and "</think>" in text:
        start_idx = text.find("<think>")
        end_idx = text.find("</think>") + len("</think>")
        text = text[:start_idx] + text[end_idx:]
    
    # Loại bỏ các khoảng trắng thừa ở đầu và cuối
    text = text.strip()
    
    return text