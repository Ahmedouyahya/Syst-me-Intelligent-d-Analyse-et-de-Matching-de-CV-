FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download Spacy models
RUN python -m spacy download fr_core_news_sm
RUN python -m spacy download en_core_web_sm

COPY . .

CMD ["python", "run.py"]
