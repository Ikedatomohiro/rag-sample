from dotenv import load_dotenv
import os
from openai import OpenAI
import boto3
import json

load_dotenv()


client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)
model="text-embedding-ada-002"

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('rag-sample')

def get_vector_from_openai_api(text):
    response = client.embeddings.create(input = [text], model=model).data[0].embedding
    return response

paragraphs = [
    "好きな動物はゾウです。",
    "週末は映画を見て過ごします。おすすめは、ハリーポッターです。",
    "最近はプログラミングの勉強をしています。",
]

for i, paragraph in enumerate(paragraphs):
    vector = get_vector_from_openai_api(paragraph)
    table.put_item(
        Item={
            'id': str(i),
            'vector': json.dumps(vector),
            'paragraph': paragraph,
            'source': 'IDEA Ver.3.1マニュアル第1部.pdf',
        }
    )
