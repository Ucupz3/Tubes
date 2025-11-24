import pickle
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split

def evaluate_model(features_path='data/features.pkl', model_path='models/sentiment_model.pkl'):
    print("Evaluating model...")
    if not os.path.exists(features_path) or not os.path.exists(model_path):
        print("Files not found.")
        return

    with open(features_path, 'rb') as f:
        X, y = pickle.load(f)
        
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
        
    # Split data (same seed as training to ensure same test set)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    y_pred = model.predict(X_test)
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    os.makedirs('plots', exist_ok=True)
    plt.savefig('plots/confusion_matrix.png')
    print("Confusion matrix saved to plots/confusion_matrix.png")
    
    # Classification Report
    report = classification_report(y_test, y_pred)
    with open('plots/classification_report.txt', 'w') as f:
        f.write(report)
    print("Classification report saved to plots/classification_report.txt")

if __name__ == "__main__":
    evaluate_model()
