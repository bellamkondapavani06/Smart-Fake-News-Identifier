import re
from typing import Tuple
from config import Config

def validate_news_input(news_text: str) -> Tuple[bool, str]:
    """
    Validates input news article text for size, length, and sanity.
    
    Returns:
        (is_valid, error_message)
    """
    if not news_text:
        return False, "Input news content cannot be empty."

    if not isinstance(news_text, str):
        return False, "Invalid input data format."

    stripped_text = news_text.strip()
    
    if len(stripped_text) < Config.MIN_INPUT_CHARS:
        return False, f"News text is too short. Please provide at least {Config.MIN_INPUT_CHARS} characters."

    if len(stripped_text) > Config.MAX_INPUT_CHARS:
        return False, f"News text exceeds maximum length of {Config.MAX_INPUT_CHARS} characters."

    words = [w for w in re.split(r"\s+", stripped_text) if w]
    if len(words) < Config.MIN_INPUT_WORDS:
        return False, f"Input text must contain at least {Config.MIN_INPUT_WORDS} words."

    # Basic XSS / Malicious payload detection
    if re.search(r"<\s*script[^>]*>", news_text, re.IGNORECASE):
        return False, "Potentially unsafe input detected (Script tags not allowed)."

    return True, ""
