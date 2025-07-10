# Vibe Story Creator

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://vibe-story-creator.streamlit.app/)

**Live Demo:** [https://vibe-story-creator.streamlit.app/](https://vibe-story-creator.streamlit.app/)

Generate unique story blueprints from a single vibe, using Retrieval-Augmented Generation (RAG) and generative AI.

## 🚀 Project Overview
Vibe Story Creator is a multi-agent, modular app that takes a user-provided "vibe" and:
- Retrieves semantically similar book inspirations from a vector database
- Synthesizes a detailed, structured story blueprint using an LLM (Groq API)
- Visualizes everything in an interactive Streamlit web app

> **Note:** The AI image generation feature is currently disabled in the public app.

## 🧠 RAG Architecture
This project uses a Retrieval-Augmented Generation (RAG) pipeline:
1. **Retrieval:** Finds the most semantically similar books to the user's vibe using a vector database (**Qdrant** + sentence-transformers).
2. **Augmented Generation:** Passes the retrieved books and the vibe to a Large Language Model (LLM) to generate a new, unique story blueprint.
3. **Visualization:** Presents the blueprint in a user-friendly storyboard interface.

## 🛠️ Tech Stack
- **Python**
- **Streamlit** (UI)
- **Qdrant** (vector database)
- **sentence-transformers** (embeddings)
- **Groq LLM API** (story synthesis)

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
   - Copy `config.py.example` to `config.py` and add your Groq token (see below).

## How to Get API Keys
- **Groq API Key:** [https://console.groq.com/keys](https://console.groq.com/keys)

## How to Run

You can try the app instantly here: [https://vibe-story-creator.streamlit.app/](https://vibe-story-creator.streamlit.app/)

Or run locally:
```sh
streamlit run app.py
```
- Enter your vibe in the UI and follow the prompts!

##  Sample Usage
1. Enter a vibe (e.g., "mysterious adventure in a lost world").
2. View the inspiration books retrieved from your database.
3. Generate a story blueprint.
4. Refine your vibe and iterate as desired.

## 🔒 Security
- **config.py** (with your API keys) is excluded from version control via `.gitignore`. 

## Contributing
Pull requests and suggestions are welcome! Please open an issue or PR to discuss improvements.

##  Future Plans
- Re-enable and improve AI image generation
- UI beautification and advanced visualizations
- LangChain/LangGraph integration for more complex agent flows
- More feedback loops and user controls

---
Enjoy creating stories from vibes! ✨ 
