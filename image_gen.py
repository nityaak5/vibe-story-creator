import streamlit as st
from huggingface_hub import InferenceClient
import requests
from PIL import Image
import io

try:
    hf_token = st.secrets["HF_TOKEN"]
except Exception:
    from config import HF_TOKEN
    hf_token = HF_TOKEN



def generate_image(prompt):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    
    # Check if request was successful
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")
    
    image = Image.open(io.BytesIO(response.content))
    return image