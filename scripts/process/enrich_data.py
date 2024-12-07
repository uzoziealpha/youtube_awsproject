import pandas as pd
import logging
import os
import yaml

# Load configuration
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Set up logging
logging.basicConfig(
    filename="logs/enrich_data.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Function to enrich data
def enrich_data(input_path, output_path):
    if os.path.exists(input_path):
        df = pd.read_csv(input_path)
        # Placeholder for data enrichment logic
        logging.info("Data loaded successfully.")

        # Example: adding a new column
        df['new_column'] = df['view_count'] * 2  # Replace with actual enrichment logic

        df.to_csv(output_path, index=False)
        logging.info(f"Enriched data saved to {output_path}")
    else:
        logging.error(f"Input file {input_path} not found!")

if __name__ == "__main__":
    enrich_data(config["paths"]["raw_data"], config["paths"]["processed_data"])
