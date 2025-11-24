from flask import Flask, render_template, request, jsonify
import pickle
import os
from src.preprocessor import preprocess_text
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

app = Flask(__name__)

# Load model and vectorizer
model_path = 'models/sentiment_model.pkl'
vectorizer_path = 'models/vectorizer.pkl'

model = None
vectorizer = None

# Initialize Sastrawi
stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()
stopword_factory = StopWordRemoverFactory()
stopword_remover = stopword_factory.create_stop_word_remover()

def load_assets():
    global model, vectorizer
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        print("Model and vectorizer loaded.")
    else:
        print("Model or vectorizer not found. Please train the model first.")

def preprocess_input(text):
    # Same pipeline as training
    text = preprocess_text(text)
    text = stopword_remover.remove(text)
    if text:
        text = stemmer.stem(text)
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model or not vectorizer:
        load_assets()
        if not model or not vectorizer:
            return jsonify({'error': 'Model not loaded'}), 500

    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    processed_text = preprocess_input(text)
    features = vectorizer.transform([processed_text])
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    classes = model.classes_
    
    # Map probabilities to classes
    prob_dict = {cls: prob for cls, prob in zip(classes, probabilities)}
    
    pos_prob = prob_dict.get('positive', 0) * 100
    neg_prob = prob_dict.get('negative', 0) * 100
    
    confidence = max(probabilities) * 100
    
    return jsonify({
        'sentiment': prediction, 
        'processed_text': processed_text,
        'confidence': round(confidence, 2),
        'positive_prob': round(pos_prob, 2),
        'negative_prob': round(neg_prob, 2)
    })

if __name__ == '__main__':
    load_assets()
    app.run(debug=True, port=5000)
