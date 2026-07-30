from google import genai

# Replace with your Gemini API Key
API_KEY = "AQ.Ab8RN6Izjx8HLLDj6iyNvp3P5zMnZKKxst0a1B0V7pDAlh2QeA"

client = genai.Client(api_key=API_KEY)


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