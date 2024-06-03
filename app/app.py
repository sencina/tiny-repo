from pinecone_client import check_connection
from repository import ingest, similarity, delete_all

if __name__ == "__main__":
    # delete_all()
    # ingest("./data/design_patterns.pdf")

    print(similarity("Tell me about the decorator pattern")[0])
