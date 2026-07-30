"""
Application Constants & Status Definitions.
"""

# Prediction Result Labels
LABEL_REAL_NEWS = "Human Written - Real News"
LABEL_FAKE_NEWS = "Human Written - Fake News"
LABEL_AI_GENERATED = "AI Generated News"

# Gemini Fact-Checking Statuses
GEMINI_STATUS_VERIFIED = "Verified"
GEMINI_STATUS_FALSE = "False"
GEMINI_STATUS_UNVERIFIED = "Unverified"
GEMINI_STATUS_SKIPPED = "Skipped"
GEMINI_STATUS_ERROR = "Error"
GEMINI_STATUS_NOT_REQUIRED = "Not Required"

# HTTP Status Codes
HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_PAYLOAD_TOO_LARGE = 413
HTTP_INTERNAL_SERVER_ERROR = 500
