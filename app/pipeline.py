import PyPDF2
import shutil
# import chromadb
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.HttpClient(host="chromadb", port=8000)
collection = client.get_or_create_collection(name="pdf_collection")

def extract_text(file_path):
    text_pages = []
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text_pages.append(page.extract_text())
    return text_pages

def chunk_text(text_pages, chunk_size=500):
    chunks = []
    for page_num, text in enumerate(text_pages):
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i+chunk_size]
            chunks.append({"page": page_num, "content": chunk})
    return chunks

def embed_chunks(chunks):
    texts = [c["content"] for c in chunks]
    embeddings = model.encode(texts).tolist()
    return embeddings

def store_in_chroma(chunks, embeddings):
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"page": c["page"], "content": c["content"]} for c in chunks]
    collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)

def save_pdf(file, save_dir="/data"):
    file_path = f"{save_dir}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path
