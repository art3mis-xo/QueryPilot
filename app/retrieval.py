from sentence_transformers import SentenceTransformer
import chromadb

client = chromadb.HttpClient(host="chromadb", port=8000)
collection = client.get_or_create_collection(name="pdf_collection")

# Load the same model you used for document chunks
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_query(query: str):
    return model.encode([query]).tolist()

def search_collection(query_embedding, k=3):
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )
    return results


