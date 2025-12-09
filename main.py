import sys
import os
from src.data_collector import collect_reviews
from src.data_labeler import label_data
from src.preprocessor import process_data
from src.feature_extractor import extract_features
from src.naive_bayes_classifier import train_model
from src.evaluator import evaluate_model
from src.visualizer import visualize_data

def main():
    print("Starting Tokopedia Sentiment Analysis Pipeline...")
    
    # Step 1: Data Collection
    # Check if data already exists to avoid re-scraping every time
    if not os.path.exists('data/tokopedia_reviews_raw.csv'):
        collect_reviews()
    else:
        print("Raw data found, skipping collection (or delete file to re-scrape).")
        
    # Step 2: Labeling
    label_data()
    
    # Step 3: Preprocessing
    process_data()
    
    # Step 4: Feature Extraction
    extract_features()
    
    # Step 5: Model Training
    train_model()
    
    # Step 6: Evaluation
    evaluate_model()
    
    # Step 7: Visualization
    visualize_data()
    
    print("Pipeline completed successfully!")
    print("To run the web interface, execute: python app.py")

if __name__ == "__main__":
    main()