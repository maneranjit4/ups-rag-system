import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st
from src.rag.generation import get_answer_and_sources
from src.configs.settings import APP_TITLE, APP_SUBTITLE

# Configure the page
st.set_page_config(page_title="UPS Sustainability Q&A", page_icon="📦", layout="centered")

st.title(APP_TITLE)
st.markdown(APP_SUBTITLE)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"]:
            with st.expander("📚 View Cited Sources"):
                for source in msg["sources"]:
                    section = source['metadata'].get('Section', 'General Document')
                    st.markdown(f"**Source [{source['citation_id']}]** - *{section}*")
                    st.caption(source['page_content'])

# User input box
if prompt := st.chat_input("type your question here..."):
    
    # 1. Display User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate and Display Assistant Message
    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating answer..."):
            try:
                result = get_answer_and_sources(prompt)
                
                answer = result["answer"]
                sources = result["sources"]
                
                # Display the inline-cited answer
                st.markdown(answer)
                
                # Display the expandable sources
                with st.expander("📚 View Cited Sources"):
                    for source in sources:
                        section = source['metadata'].get('Section', 'General Document')
                        with st.expander(f"Source [{source['citation_id']}] - *{section}*"):
                            st.caption(source['page_content'])
                
                # Save to history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "sources": sources
                })
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Make sure you have run the ingestion script to build the Vector DB!")