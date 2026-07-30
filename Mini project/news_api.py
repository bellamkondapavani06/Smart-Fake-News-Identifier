import os
from google import genai

API_KEY = os.getenv("GEMINI_API_KEY", "your api key")

def get_client():
    key = os.getenv("GEMINI_API_KEY", API_KEY)
    return genai.Client(api_key=key)

def verify_news(article):

    prompt = f"""
You are an expert fact-checking assistant.

Analyze the following news claim.

News:
{article}

Instructions:
1. Verify the claim using reliable information.
2. If enough reliable evidence exists, return Verified.
3. If the claim is false, return False.
4. If there is insufficient evidence, return Unverified.
5. Do NOT guess.

Reply ONLY in this format:

Status: Verified / False / Unverified
Reason: <brief explanation>
Confidence: <0-100>%
"""

    try:
        client = get_client()
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"Gemini Error: {e}"


if __name__ == "__main__":

    article = input("Enter News:\n")

    print(verify_news(article))
