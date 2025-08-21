# Stage 1: Downloader
# This stage uses a basic image with 'wget' to download our large model files.
FROM debian:bullseye-slim AS downloader
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*
WORKDIR /downloads
RUN wget -O decoder-model.pth "https://github.com/Ishu-Kaur/Image-Caption-AI/releases/download/v2.0.2/decoder-model.pth"
RUN wget -O encoder-model.pth "https://github.com/Ishu-Kaur/Image-Caption-AI/releases/download/v2.0.2/encoder-model.pth"
RUN wget -O vocab.pkl "https://github.com/Ishu-Kaur/Image-Caption-AI/releases/download/v2.0.2/vocab.pkl"


# Stage 2: Final Application
# This is your actual application image.
FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the downloaded model files from the 'downloader' stage
COPY --from=downloader /downloads/ .

# Copy the rest of your application code
COPY . .

# Expose the port your app runs on
EXPOSE 5000

# The command to run the application
# Note: We match the port in the README.md (5000)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]