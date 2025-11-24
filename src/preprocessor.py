import pandas as pd
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import os

def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    
    # 1. Case Folding
    text = text.lower()
    
    # 2. Cleaning
    text = re.sub(r'[^a-zA-Z\s]', '', text) # Remove non-alphabetic characters
    text = re.sub(r'\s+', ' ', text).strip() # Remove extra whitespace
    
    # 3. Tokenization (Implicit in Sastrawi/NLTK usually, but we can do it explicitly if needed)
    # For Sastrawi, we pass the string.
    
    return text

def process_data(input_path='data/tokopedia_reviews_labeled.csv', output_path='data/tokopedia_reviews_processed.csv'):
    print("Preprocessing data...")
    if not os.path.exists(input_path):
        print(f"File {input_path} not found.")
        return

    df = pd.read_csv(input_path)
    
    # Initialize Sastrawi
    stemmer_factory = StemmerFactory()
    stemmer = stemmer_factory.create_stemmer()
    
    stopword_factory = StopWordRemoverFactory()
    stopword_remover = stopword_factory.create_stop_word_remover()
    
    def full_pipeline(text):
        # Basic cleaning
        text = preprocess_text(text)
        
        # 4. Stopword Removal
        text = stopword_remover.remove(text)
        
        # 5. Stemming (This can be slow, maybe skip for quick testing, but required by plan)
        # Optimization: Apply stemming only if text is not empty
        if text:
            text = stemmer.stem(text)
            
        return text

    # Apply pipeline
    # Using a smaller sample for testing if needed, but plan says all.
    # Stemming is slow. I'll add a progress indicator or just run it.
    
    print("Applying preprocessing pipeline (this may take a while)...")
    from tqdm import tqdm
    tqdm.pandas()
    df['processed_content'] = df['content'].progress_apply(full_pipeline)
    
    # Remove empty rows after processing
    df = df[df['processed_content'] != '']
    df = df.dropna(subset=['processed_content'])
    
    df.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    process_data()
