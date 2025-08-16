import torch
from torchvision import transforms
from PIL import Image
import pickle
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# Import your model classes
from model import EncoderCNN, DecoderRNN
# We also need the Vocabulary class definition to load the vocab.pkl file
from train import Vocabulary

# --- Configuration and Model Loading ---
device = torch.device("cpu") # Run on CPU

# Define the same transformations as in training
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Load vocabulary
print("--- Loading Vocabulary ---")
with open("vocab.pkl", "rb") as f:
    vocab = pickle.load(f)
print("Vocabulary loaded successfully.")

# Model parameters (must match the trained model)
embed_size = 256
hidden_size = 256
vocab_size = len(vocab)
encoder_dim = 2048

# Initialize and load the trained models
print("--- Loading Trained Models ---")
# Encoder
encoder = EncoderCNN(embed_size).to(device)
encoder.load_state_dict(torch.load("encoder-model.pth", map_location=device))
encoder.eval() # Set to evaluation mode

# Decoder
decoder = DecoderRNN(embed_size, hidden_size, vocab_size, encoder_dim).to(device)
decoder.load_state_dict(torch.load("decoder-model.pth", map_location=device))
decoder.eval() # Set to evaluation mode
print("Models loaded successfully.")

# --- Flask App Setup ---
app = Flask(__name__)

# --- THIS IS THE CORRECTED LINE FOR DEPLOYMENT ---
# It uses the environment variable set by Render for the disk,
# but falls back to 'static/uploads/' for local development.
UPLOAD_FOLDER = os.environ.get('FLASK_APP_UPLOAD_FOLDER', 'static/uploads/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# --- END OF CHANGE ---

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Prediction Function ---
def generate_caption(image_path):
    """
    Takes an image path, loads and transforms the image,
    and returns the generated caption.
    """
    try:
        # Open and preprocess the image
        image = Image.open(image_path).convert("RGB")
        image_tensor = transform(image).unsqueeze(0).to(device)
        
        # Pass through the models
        with torch.no_grad():
            features = encoder(image_tensor)
            sampled_ids = decoder.sample(features)
        
        # Convert word IDs to words
        caption_words = []
        for word_id in sampled_ids:
            word = vocab.itos[word_id]
            if word == "<START>":
                continue
            if word == "<END>":
                break
            caption_words.append(word)
            
        return " ".join(caption_words)

    except Exception as e:
        print(f"Error generating caption: {e}")
        return "Sorry, an error occurred while generating the caption."

# --- Flask Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Generate the caption
            caption = generate_caption(filepath)
            
            # Prepare result to send to the template
            result = {
                "image_path": filepath,
                "caption": caption.capitalize()
            }
            return render_template('index.html', result=result)

    return render_template('index.html', result=None)

# Run the App 
if __name__ == '__main__':
    print("--- Starting Flask Server ---")
    # This part is ignored by Gunicorn in production but used for local testing
    app.run(host='0.0.0.0', port=5000, debug=False)