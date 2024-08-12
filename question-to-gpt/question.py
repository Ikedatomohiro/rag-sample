from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)
model="text-embedding-ada-002"

q = '何の映画見ようかな'

# ChatGPTに質問
closest_text = "週末は映画を見て過ごします。おすすめは、ハリーポッターです。"
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "以下の情報に基づいて質問に答えてください: " + closest_text},
        {"role": "user", "content": q},
    ]
)
print(response)
