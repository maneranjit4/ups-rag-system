from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

PDF_PATH = BASE_DIR / "data" / "AI Enginner Use Case Document.pdf"
VECTOR_DB_PATH = BASE_DIR / "vector_stores" / "chroma_store"
BM25_INDEX_PATH = BASE_DIR / "vector_stores" / "bm25_store" / "bm25_retriever.pkl"