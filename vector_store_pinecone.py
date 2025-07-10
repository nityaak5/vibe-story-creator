import streamlit as st
import pinecone
from sentence_transformers import SentenceTransformer
import pandas as pd

class PineconeVectorStore:
    """
    Pinecone-backed vector store for semantic search over book data.
    Uses Pinecone cloud index and sentence-transformers for embeddings.
    """
    def __init__(self):
        pc = pinecone.Pinecone(api_key=st.secrets["PINECONE_API_KEY"])
        self.index = pc.Index(st.secrets["PINECONE_INDEX"])
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.df = None
        self.meta_cols = None

    def build(self, df, meta_cols, embedding_col):
        self.df = df
        self.meta_cols = meta_cols
        # Only upsert if index is empty
        if self.index.describe_index_stats()['total_vector_count'] == 0:
            print("Building Pinecone index...")
            batch_size = 100
            for start in range(0, len(df), batch_size):
                end = min(start + batch_size, len(df))
                batch = df.iloc[start:end]
                embeddings = self.model.encode(batch[embedding_col].astype(str).tolist())
                ids = [str(i) for i in range(start, end)]
                meta = batch[meta_cols].astype(str).to_dict(orient="records")
                vectors = [(id, emb, m) for id, emb, m in zip(ids, embeddings, meta)]
                self.index.upsert(vectors=vectors)
            print("Pinecone index built.")
        else:
            print("Pinecone index loaded.")

    def query(self, query_text, n_results=2):
        query_emb = self.model.encode([query_text])[0].tolist()
        results = self.index.query(vector=query_emb, top_k=n_results, include_metadata=True)
        return [match['id'] for match in results['matches']]

    def get_metadata(self, idx):
        # Retrieve metadata from Pinecone index
        res = self.index.fetch(ids=[str(idx)])
        if res and 'vectors' in res and str(idx) in res['vectors']:
            return res['vectors'][str(idx)]['metadata']
        else:
            # Fallback to local df if available
            if self.df is not None and self.meta_cols is not None:
                return self.df.iloc[int(idx)][self.meta_cols].to_dict()
            return {} 