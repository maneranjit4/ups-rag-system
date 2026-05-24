"""preprocessing + chunking of pdf for RAG pipeline"""
import re
import fitz
import pymupdf4llm

from langchain_text_splitters import Language, MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

from src.configs import (
    path_settings as paths,
    settings,
    constants
)


# Utility functions
def _get_page_nos_to_extract(pdf_path: str, start_page: int = 4) -> list:
    """
    pages to extract from the PDF. 
    by default, it starts from page 4 to skip the cover page and table of contents.
    """

    doc = fitz.open(pdf_path)

    return list(range(start_page, doc.page_count))

def _load_pdf_as_markdown(pdf_path: str, pages_to_extract: list) -> str:
    """Extracts specified pages from the PDF and converts them to markdown format."""

    return pymupdf4llm.to_markdown(pdf_path, pages=pages_to_extract)

def _clean_markdown(text: str) -> str:
    """Cleans the markdown text by removing unwanted characters and formatting."""

    # Remove "2024 | GRI*" pattern
    text = re.sub(constants.GRI2024_PATTERN, constants.BLANK_PATTERN, text) 
    # Remove lines that contain only numbers specially for page numbers at footers
    text = re.sub(constants.PAGE_NUMBER_PATTERN, constants.BLANK_PATTERN, text, flags=re.MULTILINE) 
    # Remove "==> picture [.*] intentionally omitted <==" pattern
    text = re.sub(constants.PICTURE_OMITTED_PATTERN, constants.BLANK_PATTERN, text)
    # Convert headers with bold formatting to regular markdown headers
    text = re.sub(constants.HEADER_PATTERN, constants.HEADER_REPLACEMENT, text, flags=re.MULTILINE)
    # Demote headers that are not "TOPIC-SPECIFIC STANDARDS", "GRI 2: GENERAL DISCLOSURES", or "GRI 3: MATERIAL TOPICS"
    text = re.sub(constants.DEMOTED_HEADER_PATTERN, constants.DEMOTED_HEADER_REPLACEMENT, text, flags=re.MULTILINE)
    # Demote any "###" headers that do not start with a pattern like "1-1 ", "2-3 ", etc. to "####"
    text = re.sub(constants.SUBSECTION_PATTERN, constants.SUBSECTION_REPLACEMENT, text, flags=re.MULTILINE)
    # Replace multiple consecutive newlines with just two newlines
    text = re.sub(constants.EXTRA_NEWLINE_PATTERN, constants.EXTRA_NEWLINE_REPLACEMENT, text)

    return text.strip()

def _merge_small_chunks(chunks: list, min_chars: int = 150) -> list:
    """Merges small chunks with the subsequent chunk until the combined length meets the minimum character requirement."""

    merged_chunks = []
    held_small_chunk = None
    
    for chunk in chunks:
            
        if held_small_chunk:
            chunk.page_content = held_small_chunk.page_content + "\n\n" + chunk.page_content
            held_small_chunk = None
            
        if len(chunk.page_content.strip()) < min_chars:
            held_small_chunk = chunk
        else:
            merged_chunks.append(chunk)
            
    if held_small_chunk:
        merged_chunks.append(held_small_chunk)
        
    return merged_chunks

def _enrich_chunk_with_metadata(chunk):
    """Enriches a single chunk with metadata such as section headers"""
    if chunk.metadata:
        metadata_str = " > ".join(f"{k}: {v}" for k, v in chunk.metadata.items())
        chunk.page_content = f"{metadata_str}:\n\n{chunk.page_content}"
    return chunk

def extract_and_chunk_pdf(pdf_path: str):
    """Handles the entire pipeline from PDF to final chunks."""

    pages_to_extract = _get_page_nos_to_extract(pdf_path)
    
    raw_md_text = pymupdf4llm.to_markdown(pdf_path, pages=pages_to_extract)
    clean_md_text = _clean_markdown(raw_md_text)
    
    headers_to_split_on = constants.HEADER_SPLIT_PATTERNS
    
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False
    )
    md_header_splits = markdown_splitter.split_text(clean_md_text)
    
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.MARKDOWN, 
        chunk_size=settings.CHUNK_SIZE, 
        chunk_overlap=settings.CHUNK_OVERLAP)
    final_chunks = text_splitter.split_documents(md_header_splits)
    merged_chunks = _merge_small_chunks(final_chunks)

    enriched_chunks = [_enrich_chunk_with_metadata(chunk) for chunk in merged_chunks]
    return enriched_chunks