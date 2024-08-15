from dotenv import load_dotenv
import os
import time
from openai import OpenAI
import boto3
import json
import re
import ulid

load_dotenv()


def parse_markdown_to_dict(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # 正規表現でキーとそれに続くテキストを抽出
    pattern = r'(\d+)\n(.*?)(?=\n\d+|\Z)'  # 数字とそれに続くテキストをキャプチャ
    matches = re.findall(pattern, content, re.DOTALL)

    # 辞書に変換
    result_dict = {int(key): value.strip() for key, value in matches}

    return result_dict

# 使用例
filename = 'sanitized.md'
result_dict = parse_markdown_to_dict(filename)

# OpenAI APIを使ってテキストをベクトルに変換した結果をDynamoDBに保存
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)
model="text-embedding-ada-002"

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('kankyouhakusyo-r6')

def get_vector_from_openai_api(text):
    response = client.embeddings.create(input = [text], model=model).data[0].embedding
    return response

for i, paragraph in result_dict.items():
    vector = get_vector_from_openai_api(paragraph)
    table.put_item(
        Item={
            'id': str(ulid.new()),
            'page': str(i),
            'vector': json.dumps(vector),
            'paragraph': paragraph,
            'source': '令和６年版 環境白書・循環型社会白書・生物多様性白書 (要約)',
        }
    )
