import streamlit as st
import base64
import io

def render_image_tab(send_prompt):
    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], key="image_uploader_tab")
    if uploaded_image is not None:
        try:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_byte = buffered.getvalue()
            img_base64 = base64.b64encode(img_byte).decode()
            st.session_state["image_data"] = img_base64
        except Exception as e:
            st.error(f"Error processing image: {e}")

    with st.expander(label='Example', expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Describe this image", key="image_btn1_tab"):
                send_prompt("Describe this image", context_type="image", show_sentiment=False)
            if st.button("What objects are in this image?", key="image_btn2_tab"):
                send_prompt("What objects are in this image?", context_type="image", show_sentiment=False)
        with col2:
            if st.button("What is the mood of this image?", key="image_btn3_tab"):
                send_prompt("What is the mood of this image?", context_type="image", show_sentiment=False)
            if st.button("Generate a caption for this image", key="image_btn4_tab"):
                send_prompt("Generate a caption for this image", context_type="image", show_sentiment=False)

    st.write("##")
    image_prompt = st.chat_input(key="image_input_tab")
    if image_prompt:
        send_prompt(image_prompt, context_type="image", show_sentiment=False)