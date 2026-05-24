from langchain_groq import ChatGroq
from src.configs import settings

def get_llm():
    llm = ChatGroq(
            model=settings.LLM_MODEL, 
            temperature=0,
            max_tokens=512
        )
    return llm