import streamlit as st

def render_chat_tab(send_prompt):
    with st.expander(label='Example', expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("How do we beat bacteria?", key="chat_btn1_tab"): 
                send_prompt("How do we beat bacteria?", show_sentiment=False)
            if st.button("What is consciousness?", key="chat_btn2_tab"):
                send_prompt("What is consciousness?", show_sentiment=False)
        with col2:
            if st.button("What is the national game of India?", key="chat_btn3_tab"):
                send_prompt("What is the national game of India?", show_sentiment=False)
            if st.button("Who was the first Indian woman to win a medal at the Olympics?", key="chat_btn4_tab"):
                send_prompt("Who was the first Indian woman to win a medal at the Olympics?", show_sentiment=False)
        col3, col4 = st.columns(2)
        with col3:
            if st.button("What is the most expensive video game of all time?", key="chat_btn5_tab"):
                send_prompt("What is the most expensive video game of all time?", show_sentiment=False)
            if st.button("What's the best-selling video game console ever made?", key="chat_btn6_tab"):
                send_prompt("What's the best-selling video game console ever made?", show_sentiment=False)
        with col4:
            if st.button("Approximately from when to when was the golden age of Athens?", key="chat_btn7_tab"):
                send_prompt("Approximately from when to when was the golden age of Athens?", show_sentiment=False)
            if st.button("Who is Candragupta Maurya's grandson?", key="chat_btn8_tab"):
                send_prompt("Who is Candragupta Maurya's grandson?", show_sentiment=False)
    st.write("##")
    chat_prompt = st.chat_input(key="chat_input_tab") 
    if chat_prompt:
        send_prompt(chat_prompt)