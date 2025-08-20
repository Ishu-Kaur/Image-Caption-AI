import nltk
import pickle
from datasets import load_dataset
from tqdm import tqdm
from vocabulary import Vocabulary # This imports the class from vocabulary.py

# Tell NLTK where to find the data we downloaded in build.sh
# This is the critical fix for the server environment
nltk.data.path.append('/opt/render/project/src/nltk_data')

# This block will only run when you execute `python build_vocab.py`
if __name__ == "__main__":
    print("Starting vocabulary creation process...")
    
    # Load the Flickr8k training data from Hugging Face
    print("Loading Flickr8k dataset from Hugging Face...")
    train_dataset = load_dataset("jxie/flickr8k", split="train")
    
    # Get all captions from the dataset
    all_train_captions = Vocabulary.get_all_captions(train_dataset)
    
    # Create a vocabulary instance. We will only keep words that appear at least 5 times.
    vocab = Vocabulary(freq_threshold=5)
    vocab.build_vocabulary(all_train_captions)
    
    # Save the built vocabulary object to a file for later use
    with open("vocab.pkl", "wb") as f:
        pickle.dump(vocab, f)
        
    print("\nVocabulary creation complete!")
    print(f"Total vocabulary size: {len(vocab)}")
    print("Vocabulary saved to 'vocab.pkl'")