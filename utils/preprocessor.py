from services.preprocessing_service import PreprocessingService

def clean_text(text: str, **kwargs) -> str:
    """Wrapper function preserving backward compatibility."""
    return PreprocessingService.clean_text(text, **kwargs)
