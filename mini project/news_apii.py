from google import genai

client = genai.Client(api_key="AQ.Ab8RN6Izjx8HLLDj6iyNvp3P5zMnZKKxst0a1B0V7pDAlh2QeA")

for model in client.models.list():
    print(model.name)