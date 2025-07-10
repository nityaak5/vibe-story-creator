import streamlit as st
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, Distance, VectorParams
from sentence_transformers import SentenceTransformer
import pandas as pd

# Support both Streamlit Cloud and local config.py
try:
    qdrant_url = st.secrets["QDRANT_URL"]
    qdrant_api_key = st.secrets["QDRANT_API_KEY"]
    qdrant_collection = st.secrets["QDRANT_COLLECTION"]
except Exception:
    from config import QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION
    qdrant_url = QDRANT_URL
    qdrant_api_key = QDRANT_API_KEY
    qdrant_collection = QDRANT_COLLECTION

class QdrantVectorStore:
    """
    Qdrant-backed vector store for semantic search over book data.
    Uses Qdrant cloud collection and sentence-transformers for embeddings.
    """
    def __init__(self):
        self.client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )
        self.collection_name = qdrant_collection
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.df = None
        self.meta_cols = None

    def build(self, df, meta_cols, embedding_col):
        self.df = df
        self.meta_cols = meta_cols
        # Create collection if it doesn't exist
        if self.collection_name not in [c.name for c in self.client.get_collections().collections]:
            print("Creating Qdrant collection...")
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            batch_size = 100
            for start in range(0, len(df), batch_size):
                end = min(start + batch_size, len(df))
                batch = df.iloc[start:end]
                embeddings = self.model.encode(batch[embedding_col].astype(str).tolist())
                points = [
                    PointStruct(
                        id=int(i),
                        vector=emb.tolist(),
                        payload=batch.iloc[j][meta_cols].to_dict()
                    )
                    for j, (i, emb) in enumerate(zip(range(start, end), embeddings))
                ]
                print(f"Uploading batch {start} to {end}...")
                self.client.upsert(collection_name=self.collection_name, points=points)
            print("Qdrant collection built.")
        else:
            print("Qdrant collection loaded.")

    def query(self, query_text, n_results=2):
        query_emb = self.model.encode([query_text])[0].tolist()
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_emb,
            limit=n_results,
            with_payload=True
        )
        return [str(point.id) for point in results]

    def get_metadata(self, idx):
        # Retrieve metadata from Qdrant collection
        res = self.client.retrieve(
            collection_name=self.collection_name,
            ids=[int(idx)],
            with_payload=True
        )
        if res and len(res) > 0:
            return res[0].payload
        else:
            # Fallback to local df if available
            if self.df is not None and self.meta_cols is not None:
                return self.df.iloc[int(idx)][self.meta_cols].to_dict()
            return {} 