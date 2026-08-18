FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for OpenCV, DICOM, and Tesseract
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir sqlalchemy psycopg2-binary asyncpg alembic redis supabase "pyjwt[crypto]" "passlib[bcrypt,argon2]" langgraph structlog sse-starlette



COPY . .

EXPOSE 8000
EXPOSE 8501

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
