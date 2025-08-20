#!/bin/bash
set -e

# Install all the python packages
echo "--- Installing dependencies ---"
pip install -r requirements.txt

# Download ONLY the large model files from the GitHub Release
echo "--- Downloading model files ---"
wget -O decoder-model.pth "https://github.com/Ishu-Kaur/Image-Caption-AI/releases/download/v1.0.1/decoder-model.pth"
wget -O encoder-model.pth "https://github.com/Ishu-Kaur/Image-Caption-AI/releases/download/v1.0.1/encoder-model.pth"
echo "--- Model files downloaded successfully ---"

# CRITICAL STEP: Build the vocabulary file directly on the server
echo "--- Building vocabulary file ---"
python build_vocab.py
echo "--- Vocabulary file built successfully ---"