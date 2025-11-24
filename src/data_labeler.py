import pandas as pd
import os

def label_data(input_path='data/tokopedia_reviews_raw.csv', output_path='data/tokopedia_reviews_labeled.csv'):
    print("Labeling data...")
    if not os.path.exists(input_path):
        print(f"File {input_path} not found.")
        return

    df = pd.read_csv(input_path)
    
    # Label: 1-3 -> negative, 4-5 -> positive
    # We can use 0 for negative and 1 for positive for ML models
    def get_sentiment(score):
        if score <= 3:
            return 'negative'
        else:
            return 'positive'

    df['sentiment'] = df['score'].apply(get_sentiment)
    
    # Also create a numeric label for model training if needed, but string is fine for now or we encode later
    # Let's keep it simple
    
    df.to_csv(output_path, index=False)
    print(f"Labeled data saved to {output_path}")
    print(df['sentiment'].value_counts())

if __name__ == "__main__":
    label_data()
