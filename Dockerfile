FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements_backend.txt .
RUN pip install --no-cache-dir -r requirements_backend.txt

# Copy project files
COPY . .

# Expose ports for FastAPI and Streamlit
EXPOSE 8000
EXPOSE 8501

# Start both FastAPI and Streamlit
# We use a simple shell script to run both in the background
CMD ["sh", "-c", "uvicorn src.api.main:app --host 0.0.0.0 --port 8000 & streamlit run dashboard/app.py --server.port 8501 --server.address 0.0.0.0"]