# To run: streamlit run storyboard_sample.py
import streamlit as st

# Sample story blueprint
def get_sample_blueprint():
    return {
        "title": "The Vibe Adventure",
        "characters": ["The Dreamer", "The Guide", "The Shadow"],
        "plot": "A journey unfolds where the protagonist faces challenges, discovers secrets, and grows.",
        "setting": "A world blending the elements of the retrieved books.",
        "themes": ["Discovery", "Growth", "Adventure"]
    }

blueprint = get_sample_blueprint()

st.title(blueprint["title"])
st.subheader("Themes: " + ", ".join(blueprint["themes"]))
st.markdown(f"**Setting:** {blueprint['setting']}")
st.markdown(f"**Plot:** {blueprint['plot']}")

st.subheader("Characters")
cols = st.columns(len(blueprint["characters"]))
for i, char in enumerate(blueprint["characters"]):
    with cols[i]:
        st.markdown(f"### {char}")
        # Optionally, add images or icons here 