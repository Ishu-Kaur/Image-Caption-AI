import nltk
from collections import Counter
from tqdm import tqdm

class Vocabulary:
    def __init__(self, freq_threshold):
        self.itos = {0: "<PAD>", 1: "<START>", 2: "<END>", 3: "<UNK>"}
        self.stoi = {"<PAD>": 0, "<START>": 1, "<END>": 2, "<UNK>": 3}
        self.freq_threshold = freq_threshold

    def __len__(self):
        return len(self.itos)

    @staticmethod
    def get_all_captions(dataset):
        all_captions = []
        print("Gathering all captions from the training set...")
        for item in tqdm(dataset):
            all_captions.append(item['caption_0'])
            all_captions.append(item['caption_1'])
            all_captions.append(item['caption_2'])
            all_captions.append(item['caption_3'])
            all_captions.append(item['caption_4'])
        return all_captions
   
    def build_vocabulary(self, sentence_list):
        frequencies = Counter()
        idx = 4
        print("Tokenizing and counting word frequencies...")
        for sentence in tqdm(sentence_list):
            for word in nltk.word_tokenize(sentence.lower()):
                frequencies[word] += 1
        
        print("Building word-to-index mapping...")
        for word, count in tqdm(frequencies.items()):
            if count >= self.freq_threshold:
                self.stoi[word] = idx
                self.itos[idx] = word
                idx += 1