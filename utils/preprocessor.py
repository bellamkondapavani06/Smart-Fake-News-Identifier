import re
import html
import string

# Optional Emoji handling
try:
    import unicodedata
except ImportError:
    unicodedata = None


COMMON_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than",
    "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there",
    "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this",
    "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't",
    "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's",
    "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom",
    "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll",
    "you're", "you've", "your", "yours", "yourself", "yourselves"
}

def remove_emojis_and_non_ascii(text: str) -> str:
    """Removes emoji characters and non-printable unicode control symbols."""
    # Filter out emoji unicode categories
    cleaned_chars = []
    for char in text:
        cat = unicodedata.category(char) if unicodedata else ""
        if not (cat.startswith("So") or cat.startswith("Cs") or cat.startswith("Cn")):
            cleaned_chars.append(char)
    return "".join(cleaned_chars)

def clean_text(
    text: str,
    lower: bool = True,
    remove_urls: bool = True,
    remove_html: bool = True,
    remove_numbers: bool = True,
    remove_punctuation: bool = True,
    remove_stopwords: bool = False,
    preserve_structure: bool = False
) -> str:
    """
    Centralized, robust text preprocessing function.
    
    Args:
        text (str): Raw input news text.
        lower (bool): Lowercase text. Defaults to True.
        remove_urls (bool): Remove web URLs. Defaults to True.
        remove_html (bool): Remove HTML tags and unescape entities. Defaults to True.
        remove_numbers (bool): Remove numeric digits. Defaults to True.
        remove_punctuation (bool): Remove punctuation marks. Defaults to True.
        remove_stopwords (bool): Remove common English stopwords. Defaults to False.
        preserve_structure (bool): If True, preserves text formatting suitable for Transformers.
        
    Returns:
        str: Cleaned and normalized text.
    """
    if not isinstance(text, str) or not text.strip():
        return ""

    # 1. Unescape HTML entities & strip tags
    if remove_html:
        text = html.unescape(text)
        text = re.sub(r"<[^>]+>", " ", text)

    # 2. Lowercase
    if lower:
        text = text.lower()

    # 3. Remove URLs & email addresses
    if remove_urls:
        text = re.sub(r"http\S+|www\.\S+|mailto:\S+", " ", text)
        text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", " ", text)

    # 4. Remove emojis & non-ASCII non-text symbols
    text = remove_emojis_and_non_ascii(text)

    # 5. Remove numbers
    if remove_numbers and not preserve_structure:
        text = re.sub(r"\d+", " ", text)

    # 6. Remove punctuation
    if remove_punctuation and not preserve_structure:
        text = text.translate(str.maketrans("", "", string.punctuation))

    # 7. Normalize whitespaces
    text = re.sub(r"\s+", " ", text).strip()

    # 8. Optional Stopwords Removal
    if remove_stopwords:
        tokens = [word for word in text.split() if word not in COMMON_STOPWORDS]
        text = " ".join(tokens)

    return text
