import pandas as pd
from sentence_transformers import SentenceTransformer

class VectorStore:
    """
    Abstract base class for a vector store.
    """
    def build(self, df, meta_cols, embedding_col):
        raise NotImplementedError

    def query(self, query_text, n_results=2):
        raise NotImplementedError

    def get_metadata(self, idx):
        raise NotImplementedError

class ChromaDBVectorStore(VectorStore):
    """
    ChromaDB-backed vector store for semantic search over book data.
    Persists the collection to disk and only builds if not already present.
    """
    def __init__(self, persist_path="chroma_db", collection_name="books", embedding_model_name='all-MiniLM-L6-v2'):
        import chromadb
        #persistentClient makes sure that the collection is not built again if it already exists
        self.chroma_client = chromadb.PersistentClient(path=persist_path)
        self.collection = self.chroma_client.get_or_create_collection(name=collection_name)
        self.model = SentenceTransformer(embedding_model_name)
        self.meta_cols = None
        self.df = None

    def build(self, df, meta_cols, embedding_col):
        self.meta_cols = meta_cols
        self.df = df
        if self.collection.count() == 0:
            print("Building ChromaDB collection...")
            batch_size = 1000
            for start in range(0, len(df), batch_size):
                end = min(start + batch_size, len(df))
                batch = df.iloc[start:end]
                embeddings = self.model.encode(batch[embedding_col].astype(str).tolist())
                batch_meta = batch[self.meta_cols].astype(str).to_dict(orient="records")
                self.collection.add(
                    documents=batch[embedding_col].astype(str).tolist(),
                    embeddings=embeddings.tolist(),
                    metadatas=batch_meta,
                    ids=[str(i) for i in range(start, end)]
                )
            print("ChromaDB collection built and persisted.")
        else:
            print("ChromaDB collection loaded from disk.")

    def query(self, query_text, n_results=2):
        vibe_embedding = self.model.encode([query_text])[0].tolist()
        results = self.collection.query(query_embeddings=[vibe_embedding], n_results=n_results)
        return results['ids'][0]

    def get_metadata(self, idx):
        # Assumes self.df is loaded and idx is string/int index
        return self.df.iloc[int(idx)][self.meta_cols].to_dict() 