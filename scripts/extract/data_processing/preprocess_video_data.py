import pandas as pd

def preprocess_video_data(file_path):
    try:
        df = pd.read_csv(file_path)
        print("Video data loaded successfully.")
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: No data to parse in {file_path}.")
        return None
    
    # Fill or handle missing data as necessary
    df['view_count'] = df['view_count'].fillna(df['view_count'].mean())
    df['like_count'] = df['like_count'].fillna(df['like_count'].mean())
    df['category_id'] = df['category_id'].fillna(df['category_id'].mode()[0])
    df['description'] = df['description'].fillna("")
    
    return df

# Example usage
if __name__ == "__main__":
    video_df = preprocess_video_data('data/raw/merged_user_video_data.csv')
