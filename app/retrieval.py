# from sentence_transformers import SentenceTransformer
# import chromadb

# client = chromadb.HttpClient(host="chromadb", port=8000)
# collection = client.get_or_create_collection(name="pdf_collection")

# # Load the same model you used for document chunks
# model = SentenceTransformer("all-MiniLM-L6-v2")

# def embed_query(query: str):
#     return model.encode([query]).tolist()

# def search_collection(query_embedding, k=3):
#     results = collection.query(
#         query_embeddings=query_embedding,
#         n_results=k
#     )
#     return results

# def search_collection(query: str, k: int = 3):
#     # Placeholder — will call VPS later
#     return [
#         "This is a placeholder context chunk."
#         "Vector DB will be connected later."
#     ]

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_query(query: str):
    return model.encode(query).tolist()

def search_collection(query_embedding, k: int = 3):
    """
    TEMPORARY retrieval stub.
    Replace this with Pinecone / Qdrant / Chroma HTTP later.
    """
    return {
        "documents": [[
            "This is a placeholder context chunk."
            "Vector database will be connected later."
        ]],
        "metadatas": [[
            {"content": "This is a placeholder context chunk."},
            {"content": "Vector database will be connected later."}
        ]]
    }

