import os
import pandas as pd

def preprocess_user_behavior_data(file_path):
    try:
        user_behavior_df = pd.read_csv(file_path)
        print("User behavior data loaded successfully.")
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: No data to parse in {file_path}.")
        return None
    
    # Ensure the necessary columns exist
    required_columns = ['video_id', 'watch_time', 'average_view_duration', 'likes', 'dislikes', 'comments', 'CTR', 'shares', 'audience_retention', 'device_type', 'traffic_source']
    missing_columns = [col for col in required_columns if col not in user_behavior_df.columns]
    
    if missing_columns:
        print(f"Warning: The following required columns are missing in the data: {missing_columns}")
        user_behavior_df = user_behavior_df.drop(columns=missing_columns, errors='ignore')
    
    # Aggregate data
    user_metrics = user_behavior_df.groupby('video_id').agg({
        'watch_time': 'sum',
        'average_view_duration': 'mean',
        'likes': 'sum',
        'dislikes': 'sum',
        'comments': 'sum',
        'CTR': 'mean',
        'shares': 'sum',
        'audience_retention': 'mean',
        'device_type': lambda x: x.mode()[0] if not x.mode().empty else None,
        'traffic_source': lambda x: x.mode()[0] if not x.mode().empty else None
    }).reset_index()
    
    # Ensure the directory exists
    output_dir = 'data/processed/'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'user_metrics.csv')
    
    # Save the processed user metrics to a CSV for further use
    user_metrics.to_csv(output_path, index=False)
    print(f"User metrics data saved to {output_path}.")
    
    return user_metrics

# Example usage
if __name__ == "__main__":
    preprocess_user_behavior_data('data/raw/user_behavior_data.csv')
