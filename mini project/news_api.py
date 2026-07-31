from google import genai

API_KEY = ""

client = genai.Client(api_key=API_KEY)

def verify_news(article):

    prompt = f"""
You are a professional fact-checking assistant.

Your job is to verify the news using the latest reliable information available.

Rules:
1. Check whether the event has actually happened.
2. Never guess.
3. If the claim is supported by reliable information, return TRUE NEWS.
4. If the claim is contradicted by reliable information, return FAKE NEWS.
5. If there is not enough reliable information, return NOT ENOUGH INFORMATION.
6. Give a short reason.

News:
{article}

Reply exactly in this format:

Status:
Reason:
"""

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Gemini Error: {e}"