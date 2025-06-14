FROM python:3.9-slim

WORKDIR /app

# Install essential packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install dependencies with better timeout and retry settings
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=300 --retries 10 \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    requests beautifulsoup4 pandas numpy lxml

# Copy the rest of the application
COPY . .

# Output directory
RUN mkdir -p /data/output

# Set volume mount point
VOLUME /data

CMD ["python", "diverse_scraper.py"]