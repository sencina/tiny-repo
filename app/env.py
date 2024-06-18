from dotenv import dotenv_values, load_dotenv

load_dotenv()

PINECONE_INDEX_NAME = dotenv_values(".env")["PINECONE_INDEX_NAME"]
PINECONE_API_KEY = dotenv_values(".env")["PINECONE_API_KEY"]

OPENAI_API_KEY = dotenv_values(".env")["OPENAI_API_KEY"]
