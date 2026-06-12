from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = OpenAIEmbeddings(
    model = 'text-embedding-3-large',
    dimensions=10
)

texts = [
    'Hello , my name is Rithik',
    'I am Learning Generative AI',
    'I am Charmer & Attractive'
]

vector = embedding.embed_query('You are going to learn Gen AI')

# vector = embedding.embed_documents(texts) or use as embed_documents

print(vector)