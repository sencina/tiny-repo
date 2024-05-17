from pinecone_client import check_connection
from repository import ingest, similarity, delete_all

if __name__ == "__main__":
    delete_all()
    ingest("./data/ENSAYO_CECAM.pdf")

    #print(similarity("Cual es el número de grupo?")[0])
