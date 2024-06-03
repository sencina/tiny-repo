from pinecone_client import check_connection
from ingest import ingest, similarity, init_db

if __name__ == "__main__":
    # db = ingest("./data/design_patterns.pdf")

    print(similarity(init_db(), "Tell me about the decorator pattern")[0])
