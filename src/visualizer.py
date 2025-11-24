import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

def visualize_data(data_path='data/tokopedia_reviews_processed.csv'):
    print("Visualizing data...")
    if not os.path.exists(data_path):
        print(f"File {data_path} not found.")
        return

    df = pd.read_csv(data_path)
    
    # Sentiment Distribution
    plt.figure(figsize=(6, 6))
    df['sentiment'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['#ff9999','#66b3ff'])
    plt.title('Sentiment Distribution')
    plt.ylabel('')
    os.makedirs('plots', exist_ok=True)
    plt.savefig('plots/sentiment_distribution.png')
    print("Sentiment distribution saved to plots/sentiment_distribution.png")
    
    # Word Cloud
    def generate_wordcloud(text, title, filename):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(str(text))
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title)
        plt.savefig(filename)
        print(f"Wordcloud saved to {filename}")

    positive_text = ' '.join(df[df['sentiment'] == 'positive']['processed_content'].astype(str))
    negative_text = ' '.join(df[df['sentiment'] == 'negative']['processed_content'].astype(str))
    
    if positive_text:
        generate_wordcloud(positive_text, 'Positive Reviews Word Cloud', 'plots/wordcloud_positive.png')
    if negative_text:
        generate_wordcloud(negative_text, 'Negative Reviews Word Cloud', 'plots/wordcloud_negative.png')

if __name__ == "__main__":
    visualize_data()
