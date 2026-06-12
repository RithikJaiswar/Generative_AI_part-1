from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
)

texts = [
    'Hello , my name is Rithik',
    'I am Learning Generative AI',
    'I am Charmer & Attractive'
]

vector = embeddings.embed_documents(texts) # 384 dimensions

print(vector)