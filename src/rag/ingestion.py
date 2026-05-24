import os
import pickle
import sys
from pathlib import Path

# Ensure the repository root is on sys.path when running this file directly
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from langchain_community.retrievers import BM25Retriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from src.configs import (
    path_settings as paths,
    constants,
    settings
)
from src.rag.preprocessing import extract_and_chunk_pdf
from src.model_factory.embedding_model import get_embedding_model

def process_and_ingest():

    if not paths.VECTOR_DB_PATH.exists():
        os.makedirs(paths.VECTOR_DB_PATH)

    if not paths.BM25_INDEX_PATH.parent.exists():
        os.makedirs(paths.BM25_INDEX_PATH.parent)

    # 1. Preprocessing (Delegated to the new file)
    chunks = extract_and_chunk_pdf(str(paths.PDF_PATH))

    # 2. Embedding & Storage
    embedding_model = get_embedding_model()
    
    Chroma.from_documents(
        documents=chunks, 
        embedding=embedding_model, 
        collection_name=settings.COLLECTION_NAME,
        persist_directory=str(paths.VECTOR_DB_PATH)
    )

    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = settings.TOP_K

    with open(paths.BM25_INDEX_PATH, 'wb') as f:
        pickle.dump(bm25_retriever, f)

if __name__ == "__main__":
    process_and_ingest()
