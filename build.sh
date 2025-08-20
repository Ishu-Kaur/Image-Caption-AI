#!/bin/bash
set -e

# Install all the python packages
echo "--- Installing dependencies ---"
pip install -r requirements.txt

# Download the large model files from the GitHub Release
echo "--- Downloading model files ---"
wget -O decoder-model.pth "https://github.com/Ishu-Kaur/Image-Caption-AI/releases/download/v1.0.1/decoder-model.pth"
wget -O encoder-model.pth "https://github.com/Ishu-Kaur/Image-Caption-AI/releases/download/v1.0.1/encoder-model.pth"
wget -O vocab.pkl "https://github.com/Ishu-Kaur/Image-Caption-AI/releases/download/v1.0.1/vocab.pkl"

echo "--- All files downloaded successfully ---"