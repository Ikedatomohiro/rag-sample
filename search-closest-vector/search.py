from dotenv import load_dotenv
import os
import json
from openai import OpenAI
import boto3
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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
    table = dynamodb.Table('rag-sample')
    response = table.scan()
    items = response['Items']

    # ベクトル部分のみを抽出
    embeddings = [json.loads(item['vector']) for item in items]

    # 最も近いテキストを特定
    cosine_similarities = cosine_similarity([question_embedding], embeddings)
    closest_idx = np.argmax(cosine_similarities)
    return items[closest_idx]

q = '何の映画見ようかな'
res = lambda_handler({'question': q})
