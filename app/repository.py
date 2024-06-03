from langchain_community.document_loaders import PDFMinerLoader

from env import PINECONE_INDEX_NAME
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

__db = PineconeVectorStore(embedding=OpenAIEmbeddings(), index_name=PINECONE_INDEX_NAME)

def get_db():
    return __db

def ingest(doc_path: str):
    loader = PDFMinerLoader(doc_path)
    pages = loader.load_and_split()

    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)

    docs = text_splitter.split_documents(pages)
    docsearch = get_db().add_documents(docs)

    return docsearch

def similarity(str):
    return get_db().similarity_search(str)

def delete_all():
    res = get_db().delete(delete_all=True)
    return res

def get_retriever():
    return get_db().as_retriever(kwargs={"k": 3})
