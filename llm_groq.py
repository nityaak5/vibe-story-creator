import streamlit as st
import requests

#instead of config, we use st.secrets



def groq_llm(prompt, model="llama3-8b-8192"):
    groq_api_key = st.secrets["GROQ_API_KEY"]
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    try:
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("Groq LLM API error:", e)
        print("Response:", response.text)
        return "[LLM Error: Could not generate story blueprint.]" 