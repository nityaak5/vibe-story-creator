import pandas as pd
from vector_store import ChromaDBVectorStore
from story_synthesizer import StorySynthesizer
from llm_groq import groq_llm

def main():
    # Load your Excel file
    books_df = pd.read_excel("books.xlsx")
    meta_cols = ['Title', 'Genre', 'Description']

    # Initialize and build/load the vector store
    vector_store = ChromaDBVectorStore()
    vector_store.build(books_df, meta_cols, embedding_col='Description')

    # Query
    vibe = input("Enter the vibe for your story: ")
    top_ids = vector_store.query(vibe, n_results=2)
    retrieved_books = [vector_store.get_metadata(idx) for idx in top_ids]

    # Print inspiration titles and descriptions
    print("\nInspiration Books:")
    for i, book in enumerate(retrieved_books, 1):
        print(f"{i}. {book['Title']}\n   {book['Description']}\n")

    # Feedback loop for story blueprint
    synthesizer = StorySynthesizer(llm=groq_llm)
    while True:
        blueprint = synthesizer.synthesize(vibe, retrieved_books)
        print("\nGenerated Story Blueprint:")
        print(blueprint['story_blueprint'])
        feedback = input("\nAre you happy with this blueprint? (yes/no): ")
        if feedback.lower() == "yes":
            break
        else:
            vibe = input("Enter a refined vibe or press Enter to use the same: ") or vibe

if __name__ == "__main__":
    main() 