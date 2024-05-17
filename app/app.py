from pinecone_client import check_connection
from ingest import ingest, similarity, init_db

if __name__ == "__main__":
    ingest("./data/ENSAYO_CECAM.pdf")

    #print(similarity("Cual es el número de grupo?")[0])
