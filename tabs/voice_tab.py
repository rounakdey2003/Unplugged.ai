import streamlit as st
import pyttsx3
import speech_recognition as sr
import time

def text_to_speech(text):
    """Convert text to speech"""
    try:
        st.session_state["speaking"] = True
        st.session_state["status_message"] = "Speaking..."
        engine = pyttsx3.init()
        
        voice_speed = st.session_state.get("voice_speed", 175)
        engine.setProperty('rate', voice_speed)
        
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Speech error: {e}")
    finally:
        st.session_state["speaking"] = False
        st.session_state["status_message"] = ""
        
        if st.session_state.get("continuous_mode", False) and not st.session_state.get("listening", False):
            st.experimental_rerun()

def speech_to_text(send_prompt):
    """Convert speech to text and send as prompt"""
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    with microphone as source:
        st.session_state["listening"] = True
        st.session_state["status_message"] = "Listening..."
        st.experimental_rerun()
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            st.session_state["status_message"] = "Processing..."
            st.experimental_rerun()
            text = recognizer.recognize_google(audio)
            send_prompt(text)
        except sr.WaitTimeoutError:
            st.warning("No speech detected within the time limit.")
        except sr.UnknownValueError:
            st.warning("Could not understand audio")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            st.error(f"Speech to text error: {e}")
        finally:
            st.session_state["listening"] = False
            st.session_state["status_message"] = ""
            st.experimental_rerun()

def render_voice_tab(send_prompt):
    st.write("## Voice Interaction Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state["continuous_mode"] = st.toggle(
            "Continuous Mode", 
            value=st.session_state.get("continuous_mode", False),
            help="In continuous mode, the assistant will automatically start listening after speaking."
        )
    with col2:
        voice_speed = st.slider(
            "Voice Speed", 
            min_value=100, 
            max_value=300, 
            value=st.session_state.get("voice_speed", 175), 
            step=25,
            key="voice_speed_slider"
        )
        st.session_state["voice_speed"] = voice_speed

    st.write("##")
    
    if st.session_state.get("status_message"): 
        st.info(st.session_state["status_message"])

    if st.session_state.get("listening", False):
        st.button("Stop Listening", on_click=lambda: setattr(st.session_state, 'listening', False), type="primary")
    elif st.session_state.get("speaking", False):
        st.warning("Speaking... (Stop functionality not fully implemented for current TTS)")
    else:
        if st.button("Start Listening", key="start_listening_voice"):
            speech_to_text(send_prompt)

    if (st.session_state.get("continuous_mode", False) and
        not st.session_state.get("listening", False) and
        not st.session_state.get("speaking", False) and
        st.session_state.get("messages") and
        st.session_state["messages"][-1]["role"] == "assistant"):
        if not hasattr(st.session_state, '_last_auto_listen_time') or \
            time.time() - st.session_state._last_auto_listen_time > 2:
            st.session_state._last_auto_listen_time = time.time()
            speech_to_text(send_prompt)

    with st.expander("Voice Command Examples (Try saying these after clicking 'Start Listening')"):
        st.markdown("- What's the weather like today?\n" \
                    "- Tell me a joke.\n" \
                    "- Summarize the PDF document.")

    # Placeholder for voice-specific chat input if needed, though primary input is speech
    # voice_prompt = st.chat_input(key="voice_chat_input", disabled=st.session_state.get("listening", False))
    # if voice_prompt:
    #     send_prompt(voice_prompt)