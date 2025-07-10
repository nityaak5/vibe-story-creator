from huggingface_hub import InferenceClient
import streamlit as st


def generate_image(prompt):
    hf_token = st.secrets["HF_TOKEN"]
    client = InferenceClient(
        provider="nebius",  # or omit for default provider
        api_key=hf_token,
    )
    image = client.text_to_image(
        prompt,
        model="stabilityai/stable-diffusion-xl-base-1.0",
    )
    return image  # This is a PIL.Image object 