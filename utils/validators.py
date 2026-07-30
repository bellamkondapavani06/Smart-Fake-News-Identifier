import re
from typing import Tuple
from config import Config
from utils.logger import logger

def validate_article_input(news_text: str) -> Tuple[bool, str]:
    """
    Validates input news article text for size, length, and security.

    Returns:
        (is_valid, error_message)
    """
    if news_text is None:
        logger.warning("Validation failed: Input news text is None.")
        return False, "Input news content cannot be null."

    if not isinstance(news_text, str):
        logger.warning("Validation failed: Input news payload is not a string.")
        return False, "Invalid input data format. Expected text string."

    stripped_text = news_text.strip()
    
    if not stripped_text:
        logger.warning("Validation failed: Empty or whitespace-only input received.")
        return False, "Input news content cannot be empty or whitespace-only."

    if len(stripped_text) < Config.MIN_INPUT_CHARS:
        logger.warning(f"Validation failed: Text length ({len(stripped_text)}) below minimum ({Config.MIN_INPUT_CHARS}).")
        return False, f"News text is too short. Please provide at least {Config.MIN_INPUT_CHARS} characters."

    if len(stripped_text) > Config.MAX_INPUT_CHARS:
        logger.warning(f"Validation failed: Text length ({len(stripped_text)}) exceeds maximum ({Config.MAX_INPUT_CHARS}).")
        return False, f"News text exceeds maximum length of {Config.MAX_INPUT_CHARS} characters."

    words = [w for w in re.split(r"\s+", stripped_text) if w]
    if len(words) < Config.MIN_INPUT_WORDS:
        logger.warning(f"Validation failed: Word count ({len(words)}) below minimum ({Config.MIN_INPUT_WORDS}).")
        return False, f"Input text must contain at least {Config.MIN_INPUT_WORDS} words."

    # XSS / Script tag detection
    if re.search(r"<\s*script[^>]*>", news_text, re.IGNORECASE):
        logger.warning("Security alert: Script tag payload detected in input news text.")
        return False, "Potentially unsafe input detected (Script tags are not allowed)."

    return True, ""
