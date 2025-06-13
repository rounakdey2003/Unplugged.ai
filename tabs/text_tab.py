import streamlit as st

def render_text_tab(send_prompt):
    text_file = st.file_uploader("Upload a Text File", type=["txt"], key="text_uploader_tab")
    if text_file is not None:
        try:
            text_file.seek(0)
            text_content = text_file.read().decode("utf-8")
            st.session_state["text_file_text"] = text_content
            st.text_area("Preview", text_content, height=300, key="text_preview_tab")
        except Exception as e:
            st.error(f"Error reading text file: {e}")

    manual_text = st.text_area("Enter text manually", st.session_state.get("manual_text", ""), key="manual_text_input_tab")
    st.session_state["manual_text"] = manual_text

    with st.expander(label='Example', expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Make summary", key="text_btn1_tab"):
                with st.container():
                    send_prompt("Make summary", context_type="text", show_sentiment=False)
            if st.button("Explain in brief", key="text_btn2_tab"):
                with st.container():
                    send_prompt("Explain in brief", context_type="text", show_sentiment=False)
        with col2:
            if st.button("Construct a conclusion", key="text_btn3_tab"):
                with st.container():
                    send_prompt("Construct a conclusion", context_type="text", show_sentiment=False)
            if st.button("Define in short", key="text_btn4_tab"):
                with st.container():
                    send_prompt("Define in short", context_type="text", show_sentiment=False)

    st.write("##")
    text_prompt = st.chat_input(key="text_input_tab")
    if text_prompt:
        send_prompt(text_prompt, context_type="text", show_sentiment=False)