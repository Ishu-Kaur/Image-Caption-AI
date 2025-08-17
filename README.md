---
title: Image Caption AI
emoji: 🖼️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000
---

# Image Caption AI

This is an end-to-end AI application that generates descriptive captions for uploaded images.

## How it Works

The application is built with a classic Encoder-Decoder architecture:
- **Encoder:** A pre-trained ResNet-50 Convolutional Neural Network (CNN) extracts visual features from the image.
- **Decoder:** A Long Short-Term Memory (LSTM) Recurrent Neural Network (RNN) with an Attention mechanism generates the caption word by word based on the image features.

## Tech Stack

- **Model:** PyTorch
- **Web Framework:** Flask
- **Deployment:** Docker, Hugging Face Spaces