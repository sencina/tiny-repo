from env import PINECONE_INDEX_NAME
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

def ingest(doc_path: str):
    loader = PyPDFLoader(doc_path)
    pages = loader.load_and_split()

    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=200, chunk_overlap=50)

    docs = text_splitter.split_documents(pages)

    db= init_db()
    docsearch = db.add_documents(docs)

    return docsearch


def similarity(str):
    db = init_db()
    return db.similarity_search(str)


def init_db():
    embeddings = OpenAIEmbeddings()

    return PineconeVectorStore(embedding=embeddings, index_name=PINECONE_INDEX_NAME)

def delete_all():
    db = init_db()
    res = db.delete(delete_all=True)
    return res
