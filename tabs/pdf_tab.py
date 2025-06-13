import streamlit as st
import base64
import PyPDF2

def render_pdf_tab(send_prompt):
    pdf_file = st.file_uploader("Upload a PDF", type=["pdf"], key="pdf_uploader_tab")
    if pdf_file is not None:
        try:
            pdf_bytes = pdf_file.read()
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)

            pdf_file.seek(0)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_text = ""
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    pdf_text += text
            st.session_state["pdf_text"] = pdf_text
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")

    with st.expander(label='Example', expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Make summary", key="pdf_btn1_tab"):
                with st.container():
                    send_prompt("Make summary", context_type="pdf", show_sentiment=False)
            if st.button("Explain in brief", key="pdf_btn2_tab"):
                with st.container():
                    send_prompt("Explain in brief", context_type="pdf", show_sentiment=False)
        with col2:
            if st.button("Construct a conclusion", key="pdf_btn3_tab"):
                with st.container():
                    send_prompt("Construct a conclusion", context_type="pdf", show_sentiment=False)
            if st.button("Define in short", key="pdf_btn4_tab"):
                with st.container():
                    send_prompt("Define in short", context_type="pdf", show_sentiment=False)

    st.write("##")
    pdf_prompt = st.chat_input(key="pdf_input_tab")
    if pdf_prompt:
        send_prompt(pdf_prompt, context_type="pdf", show_sentiment=False)