# Tokopedia Sentiment Analysis Walkthrough

I have implemented the sentiment analysis program for Tokopedia reviews as requested. The project includes data collection, preprocessing, feature extraction, model training, evaluation, visualization, and a web interface.

## Project Structure

- `src/`: Contains the source code for the pipeline.
  - [data_collector.py](file:///home/rodwell/Documents/E/src/data_collector.py): Scrapes reviews from Google Play Store.
  - [data_labeler.py](file:///home/rodwell/Documents/E/src/data_labeler.py): Labels reviews based on rating.
  - [preprocessor.py](file:///home/rodwell/Documents/E/src/preprocessor.py): Cleans and preprocesses text.
  - [feature_extractor.py](file:///home/rodwell/Documents/E/src/feature_extractor.py): Converts text to TF-IDF features.
  - [naive_bayes_classifier.py](file:///home/rodwell/Documents/E/src/naive_bayes_classifier.py): Trains the Naive Bayes model.
  - [evaluator.py](file:///home/rodwell/Documents/E/src/evaluator.py): Evaluates model performance.
  - [visualizer.py](file:///home/rodwell/Documents/E/src/visualizer.py): Generates charts and word clouds.
- [app.py](file:///home/rodwell/Documents/E/app.py): Flask application for the web interface.
- `templates/`: HTML templates.
- `static/`: CSS and JavaScript files.
- [main.py](file:///home/rodwell/Documents/E/main.py): Main script to run the entire pipeline.
- [requirements.txt](file:///home/rodwell/Documents/E/requirements.txt): List of dependencies.

## How to Run

### 1. Setup Environment

Ensure you have Python installed. Create a virtual environment and install dependencies:

```bash
python -m venv venv source venv/bin/activate  # On Windows
python -m venv venv # on Linux
venv/bin/pip install -r requirements.txt
```

### 2. Run the Pipeline

To collect data, train the model, and generate visualizations, run:

```bash
venv/bin/python main.py
```

This will:

1.  Scrape 5000 reviews (if not already present).
2.  Label and preprocess the data.
3.  Train the Naive Bayes model.
4.  Evaluate the model and save plots to `plots/`.

### 3. Run the Web Interface

To start the web application for sentiment prediction:

```bash
venv/bin/python app.py
```

Open your browser and go to `http://127.0.0.1:5000`. You can enter a review and get a sentiment prediction.

## Verification Results

- **Data Collection**: Successfully scraped 5000 reviews.
- **Model**: Naive Bayes Multinomial model trained with ~86% accuracy.
- **Web Interface**: Functional with modern UI, confidence score, and probability breakdown.
- **Preprocessing**: Completed with progress bar (took ~6 mins).

## Visualizations

After running [main.py](file:///home/rodwell/Documents/E/main.py), you will find the following in the `plots/` directory:

- `sentiment_distribution.png`: Pie chart of sentiment balance.
- `wordcloud_positive.png`: Word cloud of positive reviews.
- `wordcloud_negative.png`: Word cloud of negative reviews.
- `confusion_matrix.png`: Confusion matrix of model predictions.
- `classification_report.txt`: Detailed metrics.
