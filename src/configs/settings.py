import os
from dotenv import load_dotenv

load_dotenv()


HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "llama-3.1-8b-instant"

COLLECTION_NAME = "ups_rag_collection"

APP_TITLE = "📦 UPS GRI Report Assistant"
APP_SUBTITLE = "Ask questions about the 2024 UPS Sustainability and GRI Report."

# RAG Constraints
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 4
