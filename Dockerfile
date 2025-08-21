# Stage 1: Downloader
# This stage downloads all our large files.
FROM debian:bullseye-slim AS downloader
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*
WORKDIR /downloads

# Paste your new v2.0.3 links here
RUN wget -O decoder-model.pth "https://github.com/Ishu-Kaur/Image-Caption-AI/releases/download/v2.0.3/decoder-model.pth"
RUN wget -O encoder-model.pth "https://github.com/Ishu-Kaur/Image-Caption-AI/releases/download/v2.0.3/encoder-model.pth"
RUN wget -O vocab.pkl "https://github.com/Ishu-Kaur/Image-Caption-AI/releases/download/v2.0.3/vocab.pkl"

# Stage 2: Final Application
# This is your actual application image.
FROM python:3.11-slim

WORKDIR /app

# Set the home directory for PyTorch cache to prevent permission errors
ENV TORCH_HOME=/app/cache

# Copy the downloaded model files from the 'downloader' stage
COPY --from=downloader /downloads/ .

# Copy and install Python package requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the correct port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]