import streamlit as st
from pathlib import Path
import google.generativeai as genai

# Configure Generative AI API key
genai.configure(api_key="AIzaSyAOq6C5aYYa3Bb30DKqVMtgfQswBdmud6A")

# Set up the model
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {
  "category": "HARM_CATEGORY_HARASSMENT",
  "threshold": "BLOCK_MEDIUM_AND_ABOVE"
 },
 {
  "category": "HARM_CATEGORY_HATE_SPEECH",
  "threshold": "BLOCK_MEDIUM_AND_ABOVE"
 },
 {
  "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
  "threshold": "BLOCK_MEDIUM_AND_ABOVE"
 },
 {
  "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
  "threshold": "BLOCK_MEDIUM_AND_ABOVE"
 }
]

model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Streamlit app layout
st.title("🍃Disease Detection on Leaf Images🍃")

uploaded_file = st.file_uploader("Upload a leaf image (JPEG)")

if uploaded_file is not None:
    image_path = Path(uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if image_path.exists():
        image_parts = [
            {"mime_type": "image/jpeg", "data": image_path.read_bytes()}
        ]
        prompt_parts = [image_parts[0], "detect this disease on leaf image and give me leaf or plant name also"]

        try:
            response = model.generate_content(prompt_parts)
            st.write("**Uploaded Image:**")
            st.image(uploaded_file)
            st.write("**Detected Disease:**", response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Image not found. Please upload a valid image.")
else:
    st.write("Please upload a leaf image to get started.")
