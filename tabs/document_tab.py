import streamlit as st
from docx import Document

def render_document_tab(send_prompt):
    docx_file = st.file_uploader("Upload a DOCX", type=["docx"], key="docx_uploader_tab")
    if docx_file is not None:
        try:
            document = Document(docx_file)
            docx_text = ""
            for para in document.paragraphs:
                docx_text += para.text + "\n"
            st.session_state["docx_text"] = docx_text

            st.text_area("Preview", value=docx_text, height=300, key="docx_preview_tab")
        except Exception as e:
            st.error(f"Error reading DOCX file: {e}")

    with st.expander(label='Example', expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Make summary", key="docx_btn1_tab"):
                with st.container():
                    send_prompt("Make summary", context_type="docx", show_sentiment=False)
            if st.button("Explain in brief", key="docx_btn2_tab"):
                with st.container():
                    send_prompt("Explain in brief", context_type="docx", show_sentiment=False)
        with col2:
            if st.button("Construct a conclusion", key="docx_btn3_tab"):
                with st.container():
                    send_prompt("Construct a conclusion", context_type="docx", show_sentiment=False)
            if st.button("Define in short", key="docx_btn4_tab"):
                with st.container():
                    send_prompt("Define in short", context_type="docx", show_sentiment=False)

    st.write("##")
    docx_prompt = st.chat_input(key="docx_input_tab")
    if docx_prompt:
        send_prompt(docx_prompt, context_type="docx", show_sentiment=False)