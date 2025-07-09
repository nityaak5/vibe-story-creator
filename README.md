# Vibe Story Creator

Generate unique story blueprints and visual inspiration from a single vibe, using Retrieval-Augmented Generation (RAG) and generative AI.

## 🚀 Project Overview
Vibe Story Creator is a multi-agent, modular app that takes a user-provided "vibe" and:
- Retrieves semantically similar book inspirations from a vector database
- Synthesizes a detailed, structured story blueprint using an LLM (Groq API)
- Generates an AI image inspiration for the story (Hugging Face text-to-image)
- Visualizes everything in an interactive Streamlit web app

## 🧠 RAG Architecture
This project uses a Retrieval-Augmented Generation (RAG) pipeline:
1. **Retrieval:** Finds the most semantically similar books to the user's vibe using a vector database (ChromaDB + sentence-transformers).
2. **Augmented Generation:** Passes the retrieved books and the vibe to a Large Language Model (LLM) to generate a new, unique story blueprint.
3. **Visualization:** Presents the blueprint and an AI-generated image in a user-friendly storyboard interface.

## 🛠️ Tech Stack
- **Python**
- **Streamlit** (UI)
- **ChromaDB** (vector database)
- **sentence-transformers** (embeddings)
- **Groq LLM API** (story synthesis)
- **Hugging Face Inference API** (image generation)

## ⚡ Setup Instructions
1. **Clone the repo:**
   ```sh
   git clone https://github.com/yourusername/vibe-story-creator.git
   cd vibe-story-creator
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Prepare your data:**
   - Place your `books.xlsx` file (with columns: Title, Genre, Description, etc.) in the project root.
4. **Configure API keys:**
   - Copy `config.py.example` to `config.py` and add your Groq and Hugging Face tokens (see below).

## 🔑 How to Get API Keys
- **Groq API Key:** [https://console.groq.com/keys](https://console.groq.com/keys)
- **Hugging Face Token:** [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

## 🏃 How to Run
```sh
streamlit run app.py
```
- Enter your vibe in the UI and follow the prompts!

## 📝 Sample Usage
1. Enter a vibe (e.g., "mysterious adventure in a lost world").
2. View the inspiration books retrieved from your database.
3. Generate a story blueprint and AI image inspiration.
4. Refine your vibe and iterate as desired.

## 🔒 Security
- **config.py** (with your API keys) is excluded from version control via `.gitignore`. Never commit your secrets!

## 🤝 Contributing
Pull requests and suggestions are welcome! Please open an issue or PR to discuss improvements.

## 🎨 Future Plans
- UI beautification and advanced visualizations
- LangChain/LangGraph integration for more complex agent flows
- More feedback loops and user controls

---
Enjoy creating stories from vibes! ✨ 