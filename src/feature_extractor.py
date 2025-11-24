import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

def extract_features(input_path='data/tokopedia_reviews_processed.csv', output_path='data/features.pkl', vectorizer_path='models/vectorizer.pkl'):
    print("Extracting features...")
    if not os.path.exists(input_path):
        print(f"File {input_path} not found.")
        return

    df = pd.read_csv(input_path)
    
    # Ensure processed_content is string (handle NaN if any slipped through)
    df['processed_content'] = df['processed_content'].fillna('')
    
    vectorizer = TfidfVectorizer(max_features=5000) # Limit features for performance
    X = vectorizer.fit_transform(df['processed_content'])
    y = df['sentiment']
    
    # Save features and labels
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        pickle.dump((X, y), f)
        
    # Save vectorizer
    os.makedirs(os.path.dirname(vectorizer_path), exist_ok=True)
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
        
    print(f"Features saved to {output_path}")
    print(f"Vectorizer saved to {vectorizer_path}")
    print(f"Feature matrix shape: {X.shape}")

if __name__ == "__main__":
    extract_features()
