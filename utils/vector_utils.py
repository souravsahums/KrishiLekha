from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

def get_vectorstore(persist_dir="data/chroma_store"):
    # Ensure the persist directory exists
    os.makedirs(persist_dir, exist_ok=True)

    # Initialize the HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    # Create or load the Chroma vector store
    vectorstore = Chroma(
        collection_name="documents",
        embedding_function=embeddings,
        persist_directory=persist_dir
    )

    return vectorstore

def add_to_vectorstore(vectorstore, texts, metadatas):
    ids = [f"doc_{i}" for i in range(len(texts))]
    vectorstore.add_texts(texts, metadatas=metadatas, ids=ids)
    vectorstore.persist()
