import streamlit as st
import time
from PIL import Image
import ollama
import subprocess
import pandas as pd
import numpy as np
import altair as alt
import joblib
import os

from sentiment.emotion import predict_emotions, get_prediction_proba, emotions_emoji_dict
from tabs.text_tab import render_text_tab
from tabs.voice_tab import render_voice_tab
from tabs.image_tab import render_image_tab
from tabs.chat_tab import render_chat_tab
from tabs.pdf_tab import render_pdf_tab
from tabs.document_tab import render_document_tab

st.set_page_config(layout='centered', page_icon=Image.open('image/omenLogo.png'), initial_sidebar_state='expanded',
                   page_title='Unplugged.ai', menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "**UNplugged**:rainbow[.ai] is a offline standalone app which allow user to perform AI related things"})



st.title('**UNplugged**:rainbow[.ai]')

subtitle = '**Elevate Your Workflow with Standalone AI.**'


def stream_data():
    for word in subtitle.split(" "):
        yield word + " "
        time.sleep(0.1)


if "Stream data":
    st.write_stream(stream_data)


st.divider()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Here is the beginning"}]
if "pdf_text" not in st.session_state:
    st.session_state["pdf_text"] = ""
if "docx_text" not in st.session_state:
    st.session_state["docx_text"] = ""
if "text_file_text" not in st.session_state:
    st.session_state["text_file_text"] = ""
if "manual_text" not in st.session_state:
    st.session_state["manual_text"] = ""
if "image_data" not in st.session_state:
    st.session_state["image_data"] = ""
if "listening" not in st.session_state:
    st.session_state["listening"] = False
if "speaking" not in st.session_state:
    st.session_state["speaking"] = False
if "continuous_mode" not in st.session_state:
    st.session_state["continuous_mode"] = False
if "status_message" not in st.session_state:
    st.session_state["status_message"] = ""

available_models = [
    "deepseek-r1:", "llama3.3:", "phi4:", "llama3.2:", "llama3.1:", "mistral:", "llama3:", 
    "qwen2.5:", "qwen:", "gemma:", "qwen2.5-coder:", "qwen2:", "llava:", "gemma2:", 
    "llama2:", "phi3:", "llama3.2-vision:"
]

model_variations = {
    "deepseek-r1:": ["1.5b", "7b", "8b", "14b", "32b", "70b", "671b"],
    "llama3.3:": ["70b"],
    "phi4:": ["14b"],
    "llama3.2:": ["1b", "3b"],
    "llama3.1:": ["8b", "70b", "405b"],
    "mistral:": ["7b"],
    "llama3:": ["8b", "70b"],
    "qwen2.5:": ["0.5b", "1.5b", "3b", "7b", "14b", "32b", "72b"],
    "qwen:": ["0.5b", "1.8b", "4b", "7b", "14b", "32b", "72b", "110b"],
    "gemma:": ["2b", "7b"],
    "qwen2.5-coder:": ["0.5b", "1.5b", "3b", "7b", "14b", "32b"],
    "qwen2:": ["0.5b", "1.5b", "7b", "72b"],
    "llava:": ["7b", "13b", "34b"],
    "gemma2:": ["2b", "9b", "27b"],
    "llama2:": ["7b", "13b", "70b"],
    "phi3:": ["3.8b", "14b"],
    "llama3.2-vision:": ["11b", "90b"],
}

with st.sidebar:
    st.title("Model settings")

    model_tab1, model_tab2 = st.tabs(["Select Model", "Manage Model"])
    
    with model_tab1:
        selected_model = st.selectbox("Select model (or enter manually)", ["Enter manually"] + available_models)
        
        selected_variation = ""

        if selected_model == "Enter manually":
            custom_model = st.text_input("Enter your custom model name:")
            display_model = custom_model if custom_model else "None"
            st.session_state["selected_model"] = custom_model
            st.session_state["selected_variation"] = ""
            st.write(f"Model: :green[**{display_model}**]")
        else:
            display_model = selected_model
            st.session_state["selected_model"] = selected_model
            variations = model_variations.get(selected_model, [])
            if variations:
                selected_variation = st.selectbox("Select model variation", variations)
                st.session_state["selected_variation"] = selected_variation
            st.write(f"Model: :green[**{display_model}**] Variation: :red[**{selected_variation or 'None'}**]")

        with st.expander(label="System Detect", expanded=False):
            def run_command(cmd):
                try:
                    output = subprocess.check_output(
                        cmd, shell=True, stderr=subprocess.STDOUT, encoding='utf-8', errors='replace'
                    )
                except subprocess.CalledProcessError as e:
                    output = e.output
                return output


            cmd = "ollama list"
            output = run_command(cmd)

            st.session_state["ollama_list"] = output
            st.warning(output)
    
    with model_tab2:

        commands = ["Start", "Create", "Show", "Run", "Stop", "Pull", "Push", "List", "Live", "Copy", "Remove"]
        command = st.selectbox("Select command", commands, key="ollama_command")

        extra_input = {}

        if command == "Create":
            extra_input['modelfile'] = st.text_input("Enter the path to your Modelfile:")
        elif command == "Copy":
            extra_input['src'] = st.text_input("Enter the source model name:")
            extra_input['dest'] = st.text_input("Enter the destination model name:")

        elif command in ["Show", "Run", "Stop", "Pull", "Push", "Remove"]:
            cmd_model_select = st.selectbox("Select model (or enter manually)", ["Enter manually"] + available_models, key="cmd_model_select")

            if cmd_model_select == "Enter manually":
                custom_model = st.text_input("Enter your custom model name:", key="cmd_custom_model")
                if custom_model:
                    extra_input['model'] = custom_model
            else:
                variations = model_variations.get(cmd_model_select, [])
                if variations:
                    cmd_selected_variation = st.selectbox("Select model variation", variations, key="cmd_variation")
                    extra_input['model'] = f"{cmd_model_select}{cmd_selected_variation}"
                else:
                    extra_input['model'] = cmd_model_select

        if st.button("Execute Command"):
            if command == "Start":
                cmd = "ollama start"
            elif command == "Create":
                modelfile = extra_input.get('modelfile', '')
                cmd = f"ollama create {modelfile}" if modelfile else "ollama create"
            elif command == "Show":
                model = extra_input.get('model', '')
                cmd = f"ollama show {model}" if model else "ollama show"
            elif command == "Run":
                model = extra_input.get('model', '')
                cmd = f"ollama run {model}" if model else "ollama run"
            elif command == "Stop":
                model = extra_input.get('model', '')
                cmd = f"ollama stop {model}" if model else "ollama stop"
            elif command == "Pull":
                model = extra_input.get('model', '')
                cmd = f"ollama pull {model}" if model else "ollama pull"
            elif command == "Push":
                model = extra_input.get('model', '')
                cmd = f"ollama push {model}" if model else "ollama push"
            elif command == "List":
                cmd = "ollama list"
            elif command == "Live":
                cmd = "ollama ps"
            elif command == "Copy":
                src = extra_input.get('src', '')
                dest = extra_input.get('dest', '')
                if src and dest:
                    cmd = f"ollama cp {src} {dest}"
                else:
                    st.error("Both source and destination model names are required for the cp command.")
                    cmd = ""
            elif command == "Remove":
                model = extra_input.get('model', '')
                cmd = f"ollama rm {model}" if model else "ollama rm"
            else:
                cmd = ""
                
            if cmd:
                with st.spinner("Please wait..."):
                    output = run_command(cmd)
                    st.text_area("Command Output", output, height=200)
                    if command in ["Pull", "Push", "Remove", "Create", "Copy", "List"]:
                        cmd = "ollama list"
                        list_output = run_command(cmd)
                        st.session_state["ollama_list"] = list_output
    
    st.divider()
    with st.expander("Ollama Setup Guide", expanded=False):
        st.markdown("Step 1: Go to [Ollama.com](https://ollama.com)", unsafe_allow_html=True)
        st.write("Step 2: Download Ollama Software")
        st.write("Step 3: Install the software")
        st.write("Step 4: Open **UNplugged**:rainbow[**.ai**]")
        st.write("Step 5: Go to the 'Manage Models' tab")
        st.write("Step 6: Select an Ollama command - :red[Pull]")
        st.write("Step 7: Select model and variation")
        st.write("Step 8: :orange[Execute Command]")
        st.write("Step 9: After execution, result will be shown on command screen")
        st.write("Step 10: Go to 'Select Model' tab")
        st.write("Step 11: See available model from System Detect")
        st.write("Step 12: Select model and variation")
        st.write("Step 13: Selectn example or write any prompt to get the answer")

    st.divider()
    st.page_link(page="https://github.com/rounakdey2003", label=":blue-background[:blue[Github]]",
                     help='Teleport to Github',
                     use_container_width=False)


def analyze_sentiment(text):
    try:
        prediction = predict_emotions(text)
        probability = get_prediction_proba(text)
        emoji_icon = emotions_emoji_dict[prediction]
        confidence = np.max(probability)
        
        sentiment_model = joblib.load(open(os.path.join(os.path.dirname(__file__), "sentiment/text_emotion.pkl"), "rb"))
        proba_df = pd.DataFrame(probability, columns=sentiment_model.classes_)
        proba_df_clean = proba_df.T.reset_index()
        proba_df_clean.columns = ["emotions", "probability"]
        
        return {
            "prediction": prediction,
            "emoji": emoji_icon,
            "confidence": confidence,
            "proba_df": proba_df_clean
        }
    except Exception as e:
        st.error(f"Error analyzing sentiment: {e}")
        return None


def send_prompt(prompt, speak_response=False, context_type=None, show_sentiment=True):
    if not st.session_state.get("selected_model"):
        st.error("No valid model selected. Please select a model to continue.")
        return

    if st.session_state.selected_model in available_models and not st.session_state.get("selected_variation"):
        st.error("No valid variation selected. Please select a variation to continue.")
        return
    
    if st.session_state.selected_model in available_models:
        model_identifier = st.session_state.selected_model + st.session_state.selected_variation
    else:
        model_identifier = st.session_state.selected_model

    if "ollama_list" in st.session_state and model_identifier not in st.session_state["ollama_list"]:
        st.error(f"The model :orange[{model_identifier}] is not available. Please select a valid model or variation.")
        return

    full_prompt = prompt
    if context_type:
        full_prompt = prepare_context_prompt(prompt, context_type)
        if not full_prompt:
            return

    st.session_state.messages.append({"role": "user", "content": full_prompt})

    if show_sentiment:
        sentiment_results = analyze_sentiment(prompt)
        if sentiment_results:
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Emotion: **{sentiment_results['prediction']}** {sentiment_results['emoji']}")
                st.write(f"Confidence: **{sentiment_results['confidence']:.2f}**")
            with col2:
                fig = alt.Chart(sentiment_results['proba_df']).mark_bar().encode(
                    x='emotions', 
                    y='probability', 
                    color='emotions'
                )
                st.altair_chart(fig, use_container_width=True)
    
    start_time = time.time()

    with st.spinner('Thinking...'):
        message_placeholder = st.empty()
        response = ollama.chat(
            model=model_identifier,
            messages=st.session_state.messages
        )

        if "choices" in response:
            full_text = response["choices"][0]["message"]["content"]
        elif "message" in response:
            full_text = response["message"]["content"]
        elif "text" in response:
            full_text = response["text"]
        else:
            full_text = "Error: Unexpected response format."

    end_time = time.time()
    load = end_time - start_time
    minutes, seconds = divmod(load, 60)
    st.write(f"Think for :blue[**{int(minutes):02d}m:{int(seconds):02d}s**]")

    with st.spinner('Writing'):
        chunks = [full_text[i:i + 20] for i in range(0, len(full_text), 20)]
        animated_text = ""
        for chunk in chunks:
            animated_text += chunk
            message_placeholder.success(animated_text)
            time.sleep(0.1)

    ai_sentiment_results = analyze_sentiment(full_text)
    
    st.session_state.messages.append({"role": "assistant", "content": full_text})
    
    if speak_response:
        text_to_speech(full_text)


def prepare_context_prompt(prompt, context_type):
    if context_type == "pdf":
        pdf_context = st.session_state.get("pdf_text", "")
        if not pdf_context.strip():
            st.error("Please upload a :orange[PDF] file to continue.")
            return None
        return f"Using the following PDF content, answer the question below:\n\nPDF Content:\n{pdf_context}\n\nQuestion: {prompt}"
    
    elif context_type == "docx":
        docx_context = st.session_state.get("docx_text", "")
        if not docx_context.strip():
            st.error("Please upload a :blue[DOCX] file to continue.")
            return None
        return f"Using the following DOCX content, answer the question below:\n\nDOCX Content:\n{docx_context}\n\nQuestion: {prompt}"
    
    elif context_type == "text":
        text_file_context = st.session_state.get("text_file_text", "")
        manual_context = st.session_state.get("manual_text", "")

        combined_context = ""
        if text_file_context:
            combined_context += f"Text File Content:\n{text_file_context}\n\n"
        if manual_context:
            combined_context += f"Manual Text Input:\n{manual_context}\n\n"

        if not combined_context.strip():
            st.error("Please upload a :green[Text] file or enter manual text to continue")
            return None

        return f"Using the following Text content, answer the question below:\n\n{combined_context}Question: {prompt}"
    
    elif context_type == "image":
        image_context = st.session_state.get("image_data", "")
        if not image_context:
            st.error("Please upload an :violet[Image] to continue.")
            return None
        return f"Using the following image content (base64 encoded), answer the question below:\n\nImage Content:\n{image_context}\n\nQuestion: {prompt}"
    
    return prompt


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Chat", "PDF", "Document", "Text", "Image", "Voice"])

with tab1:
    render_chat_tab(send_prompt)

with tab2:
    render_pdf_tab(send_prompt)

with tab3:
    render_document_tab(send_prompt)

with tab4:
    render_text_tab(send_prompt)

with tab5:
    render_image_tab(send_prompt)

with tab6:
    render_voice_tab(send_prompt)

with st.expander(label='History', expanded=False):
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
