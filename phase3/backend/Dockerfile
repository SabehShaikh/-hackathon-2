# Phase 3: Todo AI Chatbot Backend
# Deployment target: HuggingFace Spaces

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 7860 (HuggingFace Spaces default)
EXPOSE 7860

# Run database migrations and start server
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 7860"]
