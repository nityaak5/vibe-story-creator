# To run: streamlit run app.py
import streamlit as st
import pandas as pd
from vector_store import ChromaDBVectorStore
from story_synthesizer import StorySynthesizer
from llm_groq import groq_llm
from image_gen import generate_image

# Load data and vector store once
@st.cache_resource
def load_vector_store():
    books_df = pd.read_excel("books.xlsx")
    meta_cols = ['Title', 'Genre', 'Description']
    vector_store = ChromaDBVectorStore()
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
        story_text = st.session_state.blueprint['story_blueprint']
        st.subheader("Generated Story Blueprint")
        st.markdown(f"```\n{story_text}\n```")

        # Image inspiration button and display
        if st.button("Generate Image Inspiration"):
            with st.spinner("Generating image..."):
                img_prompt = story_text[:300]  # Use first 300 chars of blueprint as prompt
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
                st.experimental_rerun() 