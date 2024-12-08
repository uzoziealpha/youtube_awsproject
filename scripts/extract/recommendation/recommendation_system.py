import pandas as pd
import re

def load_and_merge_data(video_metadata_path, user_behavior_path):
    """
    Load and merge video metadata and user behavior data.
    
    Args:
        video_metadata_path (str): Path to the video metadata CSV file.
        user_behavior_path (str): Path to the user behavior data CSV file.
    
    Returns:
        pd.DataFrame: Merged DataFrame containing video metadata and user behavior data.
    """
    try:
        # Load video metadata
        video_metadata = pd.read_csv(video_metadata_path)
        if video_metadata.empty:
            raise ValueError("Video metadata file is empty or contains no columns.")
        print("Video metadata loaded successfully.")
        print(f"Columns in video metadata: {video_metadata.columns.tolist()}")

        # Load user behavior data
        user_behavior = pd.read_csv(user_behavior_path)
        if user_behavior.empty:
            raise ValueError("User behavior data file is empty or contains no columns.")
        print("User behavior data loaded successfully.")
        print(f"Columns in user behavior data: {user_behavior.columns.tolist()}")

        # Preview original data before any processing
        print("\nOriginal preview of video metadata:")
        print(video_metadata.head())

        print("\nOriginal preview of user behavior data:")
        print(user_behavior.head())

        # Standardize video_id columns
        def standardize_video_id(video_id):
            if pd.isnull(video_id):
                return None  # Handle NaN values
            return re.sub(r'[^a-zA-Z0-9]', '', str(video_id)).lower()

        video_metadata['video_id'] = video_metadata['video_id'].apply(standardize_video_id)
        user_behavior['video_id'] = user_behavior['video_id'].apply(standardize_video_id)

        # Drop rows with NaN video_id in user behavior data
        user_behavior = user_behavior.dropna(subset=['video_id'])

        # Print unique video IDs after standardization
        print("\nUnique video IDs in video metadata after standardization:")
        print(video_metadata['video_id'].unique())

        print("\nUnique video IDs in user behavior data after standardization:")
        print(user_behavior['video_id'].unique())

        # Identify missing video_ids
        missing_in_metadata = user_behavior[~user_behavior['video_id'].isin(video_metadata['video_id'])]['video_id']
        missing_in_behavior = video_metadata[~video_metadata['video_id'].isin(user_behavior['video_id'])]['video_id']

        if not missing_in_metadata.empty:
            print("\nvideo_ids in user behavior data not in video metadata:")
            print(missing_in_metadata)

        if not missing_in_behavior.empty:
            print("\nvideo_ids in video metadata not in user behavior data:")
            print(missing_in_behavior)

        # Merge the data
        merged_data = pd.merge(video_metadata, user_behavior, on='video_id', how='inner')
        if merged_data.empty:
            raise ValueError("Merging resulted in an empty dataset. Check 'video_id' consistency.")
        print("Data merged successfully.")
        print(f"Columns in merged data: {merged_data.columns.tolist()}")
        
        return merged_data

    except Exception as e:
        print(f"Error loading or merging data: {e}")
        return None

# Example usage of the function
if __name__ == "__main__":
    video_metadata_path = 'data/processed/video_metadata.csv'  # Path to video metadata
    user_behavior_path = 'data/processed/preprocessed_user_behavior_data.csv'  # Path to preprocessed user behavior data

    merged_data = load_and_merge_data(video_metadata_path, user_behavior_path)

    if merged_data is not None and not merged_data.empty:
        # Proceed with further processing if data is successfully loaded and merged
        print("Proceeding with recommendation system processing...")
    else:
        print("Data merging failed. Please check the debug outputs for issues.")
