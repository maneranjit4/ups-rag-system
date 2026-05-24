

# Constants for PDF preprocessing 
BLANK_PATTERN = ""
GRI2024_PATTERN = r"2024\s*\|\s*GRI\*"
PAGE_NUMBER_PATTERN = r"^\s*\d+\s*$"
PICTURE_OMITTED_PATTERN = r"\*\*==>\s*picture\s*\[.*?\]\s*intentionally\s*omitted\s*<==\*\*"
HEADER_PATTERN = r"^(#+)\s*\*\*(.*?)\*\*\s*$"
HEADER_REPLACEMENT = r"\1 \2"
DEMOTED_HEADER_PATTERN = r"^##\s+(?!TOPIC-SPECIFIC STANDARDS|GRI 2: GENERAL DISCLOSURES|GRI 3: MATERIAL TOPICS)(.*)$"
DEMOTED_HEADER_REPLACEMENT = r"### \1"
SUBSECTION_PATTERN = r"^###\s+(?!\d+-\d+\s+)(.*)$"
SUBSECTION_REPLACEMENT = r"#### \1"
EXTRA_NEWLINE_PATTERN = r"\n{3,}"
EXTRA_NEWLINE_REPLACEMENT = "\n\n"

# Constants for chunking
HEADER_SPLIT_PATTERNS = [
        ("##", "Section"),
        ("###", "Sub_Section"),
        ("####", "Tertiary_Section") 
    ]
