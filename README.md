# YouTube AWS Project

This project extracts trending YouTube videos data using the YouTube Data API, processes the data, and uploads it to AWS S3.

## Project Structure
- `data/`: Stores raw, processed, and output data.
- `scripts/`: Contains Python scripts for data extraction, processing, and uploading.
- `spark/`: Contains Docker configuration for Spark cluster.
- `config/`: Configuration files for storing credentials and settings.
- `logs/`: Logs for tracking script execution.

## Setup Instructions
1. Install the necessary Python packages:
   ```bash
   pip install -r requirements.txt
