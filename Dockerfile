# Stage 1: Downloader
FROM debian:bullseye-slim AS downloader
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*
WORKDIR /models
# Make sure to use your latest GitHub release links here
RUN wget -O decoder-model.pth "https://github.com/Ishu-Kaur/Image-Caption-AI/releases/download/v2.0.2/decoder-model.pth"
RUN wget -O encoder-model.pth "https://github.com/Ishu-Kaur/Image-Caption-AI/releases/download/v2.0.2/encoder-model.pth"
RUN wget -O vocab.pkl "https://github.com/Ishu-Kaur/Image-Caption-AI/releases/download/v2.0.2/vocab.pkl"


# Stage 2: Final Application
# Use the Python version that matches your local environment
FROM python:3.11-slim

WORKDIR /app

# Set the home directory for PyTorch cache to prevent permission errors
ENV TORCH_HOME=/app/cache

# Copy the downloaded model files from the 'downloader' stage
COPY --from=downloader /models/ .  # <-- THIS LINE IS NOW CORRECT

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the correct port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]