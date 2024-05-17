from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import dotenv_values, load_dotenv

load_dotenv()


def ingest(doc_path: str):
    loader = PyPDFLoader(doc_path)
    pages = loader.load_and_split()

    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=200, chunk_overlap=50)

    docs = text_splitter.split_documents(pages)

    embeddings = OpenAIEmbeddings()

    PineconeVectorStore(embedding=embeddings, index_name=dotenv_values(".env")["PINECONE_INDEX_NAME"]).delete(delete_all=True)

    docsearch = PineconeVectorStore.from_documents(docs, embeddings,
                                                   index_name=dotenv_values(".env")["PINECONE_INDEX_NAME"])

    return docsearch


def similarity(db: PineconeVectorStore, str):
    return db.similarity_search(str)


def init_db():
    embeddings = OpenAIEmbeddings()

    return PineconeVectorStore(embedding=embeddings, index_name=dotenv_values(".env")["PINECONE_INDEX_NAME"])