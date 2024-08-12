from pdfminer.high_level import extract_text
from dotenv import load_dotenv
import os
from openai import OpenAI
import boto3
import json

load_dotenv()


def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text

def split_text_to_paragraphs(text):
    paragraphs = text.split('\n\n')
    return paragraphs

# pdfファイル読み込みs
pdf_path = "kankyouhakusyo.pdf"
text = extract_text_from_pdf(pdf_path)
paragraphs = split_text_to_paragraphs(text)

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

for i, paragraph in enumerate(paragraphs):
    vector = get_vector_from_openai_api(paragraph)
    table.put_item(
        Item={
            'id': str(i),
            'vector': json.dumps(vector),
            'paragraph': paragraph,
            'source': '令和６年版 環境白書・循環型社会白書・生物多様性白書 (要約)',
        }
    )
