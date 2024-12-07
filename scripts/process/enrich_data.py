import pandas as pd
import os
import logging

# Set up logging
logging.basicConfig(
    filename="logs/enrich_data.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load the raw data
def load_data(file_path):
    if not os.path.exists(file_path):
        logging.error(f"File {file_path} does not exist.")
        raise FileNotFoundError(f"{file_path} not found.")
    df = pd.read_csv(file_path)
    logging.info(f"Data loaded successfully from {file_path}.")
    return df

# Enrich the data with additional metrics and columns
def enrich_data(df):
    logging.info("Starting data enrichment process...")

    # Calculate ratio of positive to negative reviews (placeholder logic)
    df['positive_review'] = df['description'].apply(lambda x: x.count("good") + x.count("great"))
    df['negative_review'] = df['description'].apply(lambda x: x.count("bad") + x.count("horrible"))
    df['review_ratio'] = df['positive_review'] / (df['negative_review'] + 1)  # Avoid division by zero

    # Calculate reach (views + likes)
    df['reach'] = df['view_count'] + df['like_count']

    # Audience retention calculation (placeholder formula)
    df['audience_retention'] = df['view_count'] / (df['view_count'] + df['comment_count'] + 1)

    logging.info("Data enrichment completed.")
    return df

# Save the enriched data to CSV
def save_to_csv(df, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)
    logging.info(f"Enriched data saved to {file_path}.")

# Main script
if __name__ == "__main__":
    try:
        # Specify paths
        raw_data_path = "data/raw/trending_videos.csv"
        enriched_data_path = "data/processed/enriched_trending_videos.csv"

        # Load, enrich, and save the data
        df = load_data(raw_data_path)
        enriched_df = enrich_data(df)
        save_to_csv(enriched_df, enriched_data_path)

        logging.info("Data enrichment process completed successfully!")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
