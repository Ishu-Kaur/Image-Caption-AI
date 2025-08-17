#!/bin/bash

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Download model files
echo "--- Downloading models ---"
wget -O encoder-model.pth "YOUR_DIRECT_DOWNLOAD_LINK_FOR_ENCODER"
wget -O decoder-model.pth "YOUR_DIRECT_DOWNLOAD_LINK_FOR_DECODER"
wget -O vocab.pkl "YOUR_DIRECT_DOWNLOAD_LINK_FOR_VOCAB"
echo "--- Models downloaded successfully ---"
