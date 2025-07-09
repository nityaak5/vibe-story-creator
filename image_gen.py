from config import HF_TOKEN
from huggingface_hub import InferenceClient

def generate_image(prompt):
    client = InferenceClient(
        provider="nebius",  # or omit for default provider
        api_key=HF_TOKEN,
    )
    image = client.text_to_image(
        prompt,
        model="stabilityai/stable-diffusion-xl-base-1.0",
    )
    return image  # This is a PIL.Image object 