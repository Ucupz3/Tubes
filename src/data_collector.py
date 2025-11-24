from google_play_scraper import Sort, reviews
import pandas as pd
import os

def collect_reviews(app_id='com.tokopedia.tkpd', count=5000, lang='id', country='id'):
    print(f"Starting to scrape {count} reviews for {app_id}...")
    
    result, continuation_token = reviews(
        app_id,
        lang=lang,
        country=country,
        sort=Sort.NEWEST,
        count=count,
        filter_score_with=None
    )
    
    print(f"Scraped {len(result)} reviews.")
    
    df = pd.DataFrame(result)
    
    # Select relevant columns
    if not df.empty:
        df = df[['userName', 'content', 'score', 'at']]
        
        output_path = 'data/tokopedia_reviews_raw.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        df.to_csv(output_path, index=False)
        print(f"Saved reviews to {output_path}")
    else:
        print("No reviews found.")

if __name__ == "__main__":
    collect_reviews()
