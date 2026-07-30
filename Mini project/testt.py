from google import genai

API_KEY = "AQ.Ab8RN6Izjx8HLLDj6iyNvp3P5zMnZKKxst0a1B0V7pDAlh2QeA"

client = genai.Client(api_key=API_KEY)

try:
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents="Hello"
    )
    print(response.text)

except Exception as e:
    print(e)