FROM python:3.9-slim

WORKDIR /app

# Install essential packages first
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install dependencies in the correct order
RUN pip install --no-cache-dir numpy==1.23.5 && \
    pip install --no-cache-dir pandas==1.5.3 && \
    pip install --no-cache-dir scikit-learn==1.2.2 joblib==1.2.0 && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

CMD ["python", "model_training.py"]