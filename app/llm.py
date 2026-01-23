from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Missing GROQ_API_KEY in .env")
client = Groq(api_key=GROQ_API_KEY)

def generate_answer(question: str, context_chunks: list[str]):
    context = "\n\n".join(context_chunks)
    prompt = f"""
    You are a helpful assistant.
    Answer the following question using ONLY the provided context.
    If the context does not contain enough information, say "I don’t know."

    Question: {question}

    Context:
    {context}

    Answer:
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return response.choices[0].message.content