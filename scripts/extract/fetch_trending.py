import json
import pandas as pd
import yaml
from googleapiclient.discovery import build
import logging
import os

# Load API credentials and configurations
def load_config():
    with open("config/credentials.json", "r") as f:
        credentials = json.load(f)
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return credentials, config

# Set up logging
def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

# Fetch trending videos
def fetch_trending_videos(youtube_api_key, region_code, max_results):
    youtube = build("youtube", "v3", developerKey=youtube_api_key)
    response = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode=region_code,
        maxResults=max_results
    ).execute()

    videos = []
    for item in response['items']:
        video_data = {
            "video_id": item["id"],
            "title": item["snippet"]["title"],
            "channel_title": item["snippet"]["channelTitle"],
            "category_id": item["snippet"]["categoryId"],
            "published_at": item["snippet"]["publishedAt"],
            "view_count": item["statistics"].get("viewCount", 0),
            "like_count": item["statistics"].get("likeCount", 0),
            "comment_count": item["statistics"].get("commentCount", 0),
            "description": item["snippet"]["description"]
        }
        videos.append(video_data)

    return pd.DataFrame(videos)

# Save data to CSV
def save_to_csv(df, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)
    logging.info(f"Data saved to {file_path}")

# Main script
if __name__ == "__main__":
    credentials, config = load_config()
    setup_logging("logs/fetch_trending.log")

    try:
        logging.info("Fetching trending videos...")
        videos_df = fetch_trending_videos(
            youtube_api_key=credentials["youtube_api_key"],
            region_code=config["youtube"]["region_code"],
            max_results=config["youtube"]["max_results"]
        )

        logging.info("Saving trending videos to CSV...")
        save_to_csv(videos_df, config["paths"]["raw_data"])

        logging.info("Process completed successfully!")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
