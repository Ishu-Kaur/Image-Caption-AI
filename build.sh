#!/bin/bash
set -e

# Install all the python packages
echo "--- Installing dependencies ---"
pip install -r requirements.txt

# Download NLTK data to a local 'nltk_data' folder
echo "--- Downloading NLTK data ---"
python -m nltk.downloader -d nltk_data punkt

# Download the model and final vocab files from the GitHub Release
echo "--- Downloading all necessary files ---"
wget -O decoder-model.pth "https://github.com/Ishu-Kaur/Image-Caption-AI/releases/download/v2.0.2/decoder-model.pth"
wget -O encoder-model.pth "https://github.com/Ishu-Kaur/Image-Caption-AI/releases/download/v2.0.2/encoder-model.pth"
wget -O vocab.pkl "https://github.com/Ishu-Kaur/Image-Caption-AI/releases/download/v2.0.2/vocab.pkl"

echo "--- All files downloaded successfully ---"


