from dotenv import dotenv_values, load_dotenv
import os

load_dotenv()

PINECONE_INDEX_NAME = os.environ["PINECONE_INDEX_NAME"] or dotenv_values(".env")["PINECONE_INDEX_NAME"]
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"] or dotenv_values(".env")["PINECONE_API_KEY"]