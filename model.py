import torch
import torch.nn as nn
import torchvision.models as models

class EncoderCNN(nn.Module):
    def __init__(self, embed_size):
        super(EncoderCNN, self).__init__()
        # Use resnet50, a powerful pre-trained model
        resnet = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        # Freeze all the parameters in the pre-trained model
        for param in resnet.parameters():
            param.requires_grad_(False)
        
        # Remove the last two layers (the average pool and the final classifier)
        modules = list(resnet.children())[:-2]
        self.resnet = nn.Sequential(*modules)
        
    def forward(self, images):
        # Extract features with the ResNet
        features = self.resnet(images)  # Shape: (batch_size, 2048, 7, 7)
        # Reshape the features for the attention mechanism
        features = features.permute(0, 2, 3, 1)  # Shape: (batch_size, 7, 7, 2048)
        features = features.view(features.size(0), -1, features.size(-1))  # Shape: (batch_size, 49, 2048)
        return features

class Attention(nn.Module):
    def __init__(self, encoder_dim, decoder_dim, attention_dim):
        super(Attention, self).__init__()
        self.encoder_att = nn.Linear(encoder_dim, attention_dim)
        self.decoder_att = nn.Linear(decoder_dim, attention_dim)
        self.full_att = nn.Linear(attention_dim, 1)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)

    def forward(self, encoder_out, decoder_hidden):
        att1 = self.encoder_att(encoder_out)
        att2 = self.decoder_att(decoder_hidden)
        att = self.full_att(self.relu(att1 + att2.unsqueeze(1))).squeeze(2)
        alpha = self.softmax(att)
        attention_weighted_encoding = (encoder_out * alpha.unsqueeze(2)).sum(dim=1)
        return attention_weighted_encoding, alpha

# --- In model.py ---

class DecoderRNN(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size, encoder_dim=2048, drop_prob=0.5):
        super(DecoderRNN, self).__init__()
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.attention = Attention(encoder_dim, hidden_size, hidden_size)
        self.lstm = nn.LSTMCell(embed_size + encoder_dim, hidden_size)
        self.dropout = nn.Dropout(p=drop_prob)
        self.fc = nn.Linear(hidden_size, vocab_size)
        
        # --- FIX #1: Store vocab_size as an attribute ---
        self.vocab_size = vocab_size

    def forward(self, features, captions):
        embeddings = self.embed(captions)
        batch_size = features.size(0)
        h, c = torch.zeros(batch_size, self.lstm.hidden_size).to(features.device), \
               torch.zeros(batch_size, self.lstm.hidden_size).to(features.device)
        
        seq_length = len(captions[0]) - 1 
        
        # --- FIX #2: Use the stored attribute self.vocab_size ---
        predictions = torch.zeros(batch_size, seq_length, self.vocab_size).to(features.device)

        for t in range(seq_length):
            context, alpha = self.attention(features, h)
            lstm_input = torch.cat((embeddings[:, t], context), dim=1)
            h, c = self.lstm(lstm_input, (h, c))
            output = self.fc(self.dropout(h))
            predictions[:, t] = output
            
        return predictions

    # The sample method does not need changes, but is included for completeness
    def sample(self, features, max_len=20):
        batch_size = features.size(0)
        h, c = torch.zeros(batch_size, self.lstm.hidden_size).to(features.device), \
               torch.zeros(batch_size, self.lstm.hidden_size).to(features.device)
        
        output = []
        inputs = self.embed(torch.tensor([1]).to(features.device))

        for _ in range(max_len):
            context, alpha = self.attention(features, h)
            lstm_input = torch.cat((inputs, context), dim=1)
            h, c = self.lstm(lstm_input, (h, c))
            preds = self.fc(h)
            
            predicted_index = preds.argmax(1)
            output.append(predicted_index.item())
            
            if predicted_index.item() == 2: # <END> token
                break
                
            inputs = self.embed(predicted_index)

        return output
#  THIS BLOCK IS FOR TESTING ONLY. It runs when you execute `python model.py` directly.

if __name__ == '__main__':
    
    print("--- Running a test of the model definitions ---")

    # --- Test Parameters ---
    embed_size = 256
    hidden_size = 512
    vocab_size = 5000  # A typical vocabulary size
    batch_size = 4
    
    # --- Create Dummy (Fake) Inputs ---
    # A batch of fake images (batch_size, channels, height, width)
    # ResNet expects 3 channels (RGB) and 224x224 images
    fake_images = torch.randn(batch_size, 3, 224, 224) 
    
    # A batch of fake captions (batch_size, sequence_length)
    # Let's say max sequence length is 15
    fake_captions = torch.randint(0, vocab_size, (batch_size, 15))

    # --- Instantiate Models ---
    print("Instantiating Encoder and Decoder...")
    encoder = EncoderCNN(embed_size=embed_size)
    decoder = DecoderRNN(embed_size=embed_size, hidden_size=hidden_size, vocab_size=vocab_size)
    print("Models instantiated successfully.")

    # --- Run a Forward Pass Test ---
    print("\nTesting the forward pass (used during training)...")
    
    # 1. Get features from encoder
    features = encoder(fake_images)
    print(f"Encoder output shape (features): {features.shape}")

    # 2. Get predictions from decoder
    predictions = decoder(features, fake_captions)
    print(f"Decoder output shape (predictions): {predictions.shape}")

    # --- Run a Sampling Test ---
    print("\nTesting the sample method (used for inference)...")
    # Use only one feature from the batch for simplicity
    single_feature = features[0].unsqueeze(0)
    sampled_ids = decoder.sample(single_feature, max_len=20)
    print(f"Sampled caption (word indices): {sampled_ids}")
    
    print("\n--- Test Complete ---")
    print("If you see output shapes and a list of numbers without any errors, your model architecture is correct!")