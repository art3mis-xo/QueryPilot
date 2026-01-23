FROM python:3.11-slim

WORKDIR /app

RUN pip install fastapi uvicorn chromadb python-multipart PyPDF2 sentence-transformers groq

COPY app/main.py .
COPY app/requirements.txt .
COPY app/pipeline.py .
COPY app/retrieval.py .
COPY app/llm.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# FROM python:3.11-slim as builder

# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Copy requirements first for better caching
# COPY app/requirements.txt .
# # Builder stage
# RUN pip install --no-cache-dir -r requirements.txt


# FROM python:3.11-slim

# WORKDIR /app

# # Install runtime dependencies
# RUN apt-get update && apt-get install -y \
#     libpq5 \
#     && rm -rf /var/lib/apt/lists/*

# # Copy installed packages from builder stage
# COPY --from=builder /usr/local /usr/local


# # Copy application code
# COPY app/ .

# # Create non-root user
# RUN useradd --create-home --shell /bin/bash app
# USER app

# # Make sure scripts in .local are usable
# ENV PATH=/root/.local/bin:$PATH

# EXPOSE 8000

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]