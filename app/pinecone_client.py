from pinecone import Pinecone
from dotenv import dotenv_values, load_dotenv

load_dotenv()

pc = Pinecone(api_key=dotenv_values(".env")["PINECONE_API_KEY"])
index = pc.Index(dotenv_values(".env")["PINECONE_INDEX_NAME"])

def check_connection():
    return index.describe_index_stats()