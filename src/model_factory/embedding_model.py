from langchain_huggingface import HuggingFaceEmbeddings
from src.configs import settings

def get_embedding_model():
    embedding_model= HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    return embedding_model