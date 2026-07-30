from typing import Dict, Any, Optional, Tuple
from utils.constants import HTTP_OK

def format_api_response(
    success: bool,
    data: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None,
    status_code: int = HTTP_OK
) -> Tuple[Dict[str, Any], int]:
    """Formats standardized JSON API response structure."""
    payload = {
        "success": success,
        "error": error,
        "prediction": data if success else None
    }
    return payload, status_code

def safe_dict_get(d: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely retrieves key from dict with default fallback."""
    if isinstance(d, dict):
        return d.get(key, default)
    return default
