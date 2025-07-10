# To run: streamlit run app.py
import streamlit as st
import pandas as pd
from vector_store_pinecone import PineconeVectorStore
from story_synthesizer import StorySynthesizer
from llm_groq import groq_llm
from image_gen import generate_image

# --- Custom CSS for background and cards ---
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
    }
    .storyboard-card {
        background: #fff;
        color: #18181b;
        border-radius: 1rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.07);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .theme-badge {
        display: inline-block;
        background: #6366f1;
        color: #fff;
        border-radius: 0.5rem;
        padding: 0.3rem 0.8rem;
        margin-right: 0.5rem;
        font-size: 0.9rem;
    }
    .storyboard-subtitle {
        font-weight: bold;
        font-size: 1.15rem;
        margin-bottom: 0.5rem;
        color: #18181b;
    }
    .storyboard-title {
        color: #18181b;
        font-size: 2.2rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load data and vector store once
@st.cache_resource
def load_vector_store():
    books_df = pd.read_excel("books.xlsx")
    meta_cols = ['Title', 'Genre', 'Description']
    vector_store = PineconeVectorStore()
    vector_store.build(books_df, meta_cols, embedding_col='Description')
    return vector_store, books_df, meta_cols

vector_store, books_df, meta_cols = load_vector_store()
synthesizer = StorySynthesizer(llm=groq_llm)

st.title("Vibe Story Creator")
st.write("Enter a vibe to generate a unique story blueprint inspired by real books!")

if 'vibe' not in st.session_state:
    st.session_state.vibe = ''
if 'retrieved_books' not in st.session_state:
    st.session_state.retrieved_books = []
if 'blueprint' not in st.session_state:
    st.session_state.blueprint = None
if 'feedback' not in st.session_state:
    st.session_state.feedback = None
if 'image_obj' not in st.session_state:
    st.session_state.image_obj = None

vibe = st.text_input("Enter the vibe for your story:", value=st.session_state.vibe)

if vibe and st.session_state.vibe != vibe:
    # New vibe entered, reset state
    st.session_state.vibe = vibe
    top_ids = vector_store.query(vibe, n_results=2)
    st.session_state.retrieved_books = [vector_store.get_metadata(idx) for idx in top_ids]
    st.session_state.blueprint = None
    st.session_state.feedback = None
    st.session_state.image_obj = None

if st.session_state.vibe:
    st.subheader("Inspiration Books")
    for i, book in enumerate(st.session_state.retrieved_books, 1):
        st.markdown(f"**{i}. {book['Title']}**\n\n{book['Description']}")

    if st.button("Generate Story Blueprint") or st.session_state.blueprint:
        if not st.session_state.blueprint:
            with st.spinner("Generating story blueprint..."):
                st.session_state.blueprint = synthesizer.synthesize(st.session_state.vibe, st.session_state.retrieved_books)
        blueprint = st.session_state.blueprint['story_blueprint']
        st.subheader("Generated Story Blueprint")

        # --- Storyboard visualization ---
        if isinstance(blueprint, dict) and all(k in blueprint for k in ["title", "themes", "setting", "plot", "characters"]):
            st.markdown(f"<div class='storyboard-card'><div class='storyboard-title'>{blueprint['title'].upper()}</div></div>", unsafe_allow_html=True)
            st.markdown("<div class='storyboard-card'>", unsafe_allow_html=True)
            st.markdown("<span class='storyboard-subtitle'>Themes:</span> " + " ".join([f"<span class='theme-badge'>{theme}</span>" for theme in blueprint['themes']]), unsafe_allow_html=True)
            st.markdown(f"<div class='storyboard-subtitle'>Setting:</div> {blueprint['setting']}", unsafe_allow_html=True)
            st.markdown(f"<div class='storyboard-subtitle'>Plot:</div> {blueprint['plot']}", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='storyboard-card'><span class='storyboard-subtitle'>Characters</span></div>", unsafe_allow_html=True)
            char_cols = st.columns(len(blueprint['characters']))
            for i, char in enumerate(blueprint['characters']):
                with char_cols[i]:
                    st.markdown(f"<div class='storyboard-card' style='text-align:center'><b>{char}</b></div>", unsafe_allow_html=True)
        else:
            # Fallback: display as text
            st.markdown(f"<div class='storyboard-card'>{blueprint}</div>", unsafe_allow_html=True)

        # Image inspiration button and display
        if st.button("Generate Image Inspiration"):
            with st.spinner("Generating image..."):
                if isinstance(blueprint, dict) and 'setting' in blueprint and 'themes' in blueprint:
                    img_prompt = f"{blueprint['setting']}. {', '.join(blueprint['themes'])}. Beautiful, detailed environment, no people, no faces."
                else:
                    img_prompt = str(blueprint)[:300]
                st.session_state.image_obj = generate_image(img_prompt)
        if st.session_state.image_obj is not None:
            st.image(st.session_state.image_obj, caption="AI-generated inspiration", use_container_width=True)

        # Feedback loop
        st.write("Are you happy with this blueprint?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, I'm happy!"):
                st.session_state.feedback = 'yes'
        with col2:
            if st.button("No, refine vibe"):
                st.session_state.feedback = 'no'

        if st.session_state.feedback == 'yes':
            st.success("Your story is ready! 🎉")
        elif st.session_state.feedback == 'no':
            new_vibe = st.text_input("Enter a refined vibe or press Enter to use the same:", value=st.session_state.vibe, key='refine_vibe')
            if st.button("Regenerate Blueprint"):
                st.session_state.vibe = new_vibe
                st.session_state.blueprint = None
                st.session_state.feedback = None
                st.session_state.image_obj = None
                top_ids = vector_store.query(new_vibe, n_results=2)
                st.session_state.retrieved_books = [vector_store.get_metadata(idx) for idx in top_ids]
                if hasattr(st, 'rerun'):
                    st.rerun()
                else:
                    st.experimental_rerun() 