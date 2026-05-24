import pickle
from langchain_community.vectorstores import Chroma
from langchain_classic.retrievers.ensemble import EnsembleRetriever

from src.configs import (
    path_settings as paths,
    constants,
    settings
)
from src.rag.ingestion import process_and_ingest
from src.model_factory.embedding_model import get_embedding_model

def get_retriever():

    if not paths.BM25_INDEX_PATH.exists() or not paths.VECTOR_DB_PATH.exists():
        process_and_ingest()

    embedding_model = get_embedding_model()

    vector_db = Chroma(
        persist_directory=str(paths.VECTOR_DB_PATH), 
        embedding_function=embedding_model
    )
    semantic_retriever = vector_db.as_retriever(search_kwargs={"k": settings.TOP_K})

    with open(paths.BM25_INDEX_PATH, 'rb') as f:
        keyword_retriever = pickle.load(f)
    
    hybrid_retriever = EnsembleRetriever(
        retrievers=[semantic_retriever, keyword_retriever],
        weights=[0.5, 0.5]
    )

    return hybrid_retriever