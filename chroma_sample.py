import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

# Load your Excel file
books_df = pd.read_excel("books.xlsx")

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create Chroma in-memory client
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="books")

# Add in batches
batch_size = 1000
for start in range(0, len(books_df), batch_size):
    end = min(start + batch_size, len(books_df))
    batch = books_df.iloc[start:end]
    embeddings = model.encode(batch['Description'].astype(str).tolist())

    # Before adding to ChromaDB, convert all metadata columns to string
    meta_cols = ['Title', 'Genre', 'Description']  # Add more if needed
    batch_meta = batch[meta_cols].astype(str).to_dict(orient="records")

    collection.add(
        documents=batch['Description'].astype(str).tolist(),
        embeddings=embeddings.tolist(),
        metadatas=batch_meta,
        ids=[str(i) for i in range(start, end)]
    )

# Sample vibe
vibe = "girl who is a scientist"
vibe_embedding = model.encode([vibe])[0].tolist()

# Query the collection for top 2 similar books
results = collection.query(
    query_embeddings=[vibe_embedding],
    n_results=2
)

print("Top 2 similar books for vibe:", vibe)
for idx in results['ids'][0]:
    meta = books_df.iloc[int(idx)][['Title', 'Genre', 'Description']].to_dict()
    print(meta) 