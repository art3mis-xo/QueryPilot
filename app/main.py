from fastapi import FastAPI, UploadFile, Query
import shutil
# import chromadb
from pipeline import extract_text, chunk_text, embed_chunks, store_in_chroma, save_pdf
# from pipeline import store_in_chroma
from retrieval import embed_query, search_collection
from sentence_transformers import SentenceTransformer
from llm import generate_answer

app = FastAPI()

# Connect to Chroma service via HTTP
# client = chromadb.HttpClient(host="chromadb", port=8000)
# collection = client.get_or_create_collection(name="pdf_collection")
model = SentenceTransformer("all-MiniLM-L6-v2")

# @app.get("/insert")
# def insert_dummy():
#     # Insert dummy vector
#     collection.add(
#         ids=["vec1"],
#         embeddings=[[0.1, 0.2, 0.3]],
#         metadatas=[{"label": "dummy"}]
#     )
#     return {"status": "inserted"}

# @app.get("/query")
# def query_dummy():
#     results = collection.query(
#         query_embeddings=[[0.1, 0.2, 0.3]],
#         n_results=1
#     )
#     return results

@app.post("/upload")
async def upload_pdf(file: UploadFile):
    file_path = f"/data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "saved", "path": file_path}

# @app.post("/ingest")
# async def ingest_pdf(file: UploadFile):
#     file_path = save_pdf(file)              # Step 1: save
#     text_pages = extract_text(file_path)    # Step 2: extract
#     chunks = chunk_text(text_pages)         # Step 3: chunk
#     embeddings = embed_chunks(chunks)       # Step 4: embed
#     store_in_chroma(chunks, embeddings)     # Step 5: store
#     return {"status": "ingested"}

# @app.post("/ingest")
# async def ingest_pdf(file: UploadFile):
#     # Step 1: Save PDF directly to /data
#     file_path = f"/data/{file.filename}"
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     # Step 2: Extract text
#     text_pages = extract_text(file_path)
#     # Step 3: Chunk text
#     chunks = chunk_text(text_pages)
#     # Step 4: Embed chunks
#     embeddings = embed_chunks(chunks)
#     # Step 5: Store in Chroma
#     store_in_chroma(chunks, embeddings)
#     return {"status": "ingested", "chunks": len(chunks)}

@app.get("/search")
def search(query: str, k: int = 3):
    query_embedding = embed_query(query)
    results = search_collection(query_embedding, k)
    return results

@app.post("/ask")
async def ask_question(query: str):
    query_embedding = embed_query(query)
    results = search_collection(query_embedding, k=3)
    context_chunks = [meta["content"] for meta in results["metadatas"][0]]
    answer = generate_answer(query, context_chunks)
    return {"question": query, "answer": answer, "context": context_chunks}



# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from models import *
# from database import *
# from database import engine, get_db
# import os
# import models

# models.Base.metadata.create_all(bind=engine)

# app = FastAPI(title="FastAPI Docker App", version="1.0.0")

# @app.get("/")
# def read_root():
#     return {"message": "FastAPI with Docker Compose is running!"}

# @app.get("/health")
# def health_check():
#     return {"status": "healthy", "database": "connected"}

# @app.post("/items/")
# def create_item(name: str, description: str, db: Session = Depends(get_db)):
#     db_item = models.Item(name=name, description=description)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

# @app.get("/items/")
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = db.query(models.Item).offset(skip).limit(limit).all()
#     return items
