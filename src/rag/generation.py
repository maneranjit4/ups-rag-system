from langchain_classic.prompts import PromptTemplate

from src.configs import (
    path_settings as paths,
    constants,
    settings
)
from src.rag.prompts import RAG_SYSTEM_PROMPT
from src.rag.retrieval import get_retriever
from src.model_factory.llm_model import get_llm

def get_answer_and_sources(question: str) -> dict:

    llm = get_llm()

    hybrid_retriever = get_retriever()

    retrieved_docs = hybrid_retriever.invoke(question)

    formatted_context = ""
    for index, doc in enumerate(retrieved_docs):
        formatted_context += f"Document [{index + 1}]:\n{doc.page_content}\n\n"

    prompt_template = PromptTemplate(
        input_variables=["context", "input"],
        template=RAG_SYSTEM_PROMPT + "\n\nQuestion: {input}\nAnswer:"
    )
    final_prompt = prompt_template.format(
        context=formatted_context,
        input=question
    )

    response_text = llm.invoke(final_prompt)

    return {
        "answer": response_text.content,
        "sources": [
            {
                "citation_id": index + 1,
                "page_content": doc.page_content,
                "metadata": doc.metadata
            } for index, doc in enumerate(retrieved_docs)
        ]
    }