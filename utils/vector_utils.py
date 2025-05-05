import uuid
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# Load environment variables from .env file
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
qdrant_collection_name = os.getenv("QDRANT_COLLECTION_NAME", "documents")

def get_vectore_store():
    # Initialize HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    # Initialize Qdrant client for remote server

    client = QdrantClient(
        host=qdrant_url,     
        api_key=qdrant_api_key
    )

    # Recreate the collection if it doesn't exist
    if not client.collection_exists(qdrant_collection_name):
        client.recreate_collection(
            collection_name=qdrant_collection_name,
            vectors_config=VectorParams(
                size=384,  # Size of the embedding vector
                distance=Distance.COSINE,
            ),
        )

    # Wrap Qdrant with LangChain
    vectorstore = Qdrant(
        client=client,
        collection_name=qdrant_collection_name,
        embeddings=embeddings
    )

    return vectorstore

def add_to_vectorstore(vectorstore, texts, metadatas):
    ids = [str(uuid.uuid4()) for _ in texts]
    vectorstore.add_texts(texts=texts, metadatas=metadatas, ids=ids)
