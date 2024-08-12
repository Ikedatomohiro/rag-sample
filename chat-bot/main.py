import os
import json
from openai import OpenAI
import boto3
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)
model="text-embedding-ada-002"


def lambda_handler(event) -> dict:
    # 質問をベクトルに変換
    question = event['question']
    question_embedding = client.embeddings.create(input = [question], model=model).data[0].embedding

    # DynamoDBからベクトルを取得
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('kankyouhakusyo-r6')
    response = table.scan()
    items = response['Items']

    # ベクトル部分のみを抽出
    embeddings = [json.loads(item['vector']) for item in items]

    # 最も近いテキストを特定
    cosine_similarities = cosine_similarity([question_embedding], embeddings)
    closest_idx = np.argmax(cosine_similarities)
    return items[closest_idx]

# 一番近いデータを取得
q = '第１部の構成'
res = lambda_handler({'question': q})
closest_text = res['paragraph']

# ChatGPTに質問
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "以下の情報に基づいて質問に答えてください: " + closest_text},
        {"role": "user", "content": q},
    ]
)
print(response)
