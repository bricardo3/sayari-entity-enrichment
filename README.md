# Sayari Entity Enrichment

This project demonstrates how to enrich entity profiles using the Sayari API, combined with external geolocation and weather data. It's designed as a proof of concept (PoC) to simulate a real-world scenario a Solutions Engineer might encounter.

## Project Structure

- `sayari/`: Handles Sayari API authentication and search
- `utils/`: Utility functions for weather, file handling, and entity detail extraction
- `src/main.py`: Entry point for loading, processing, and exporting enriched Excel data

## Requirements

- Python 3.10+
- Required packages listed in `requirements.txt`

## How to Run

1. Clone or download this repository.
2. Install dependencies:
   pip install -r requirements.txt
3. Run the application:
python src/main.py
4. Select the input Excel file when prompted.
5. After processing, choose where to save the enriched output.

## Input File Format
The input Excel file must have at least one sheet with the following required columns (case-insensitive):
- name
- address
- country (must be ISO 3-letter country code, e.g., RUS, CHN)

## Output
The output Excel file will contain the original data plus enriched fields including:
- Sayari entity ID
- Sanctions status
- Export control flags and levels
- Related entities count
- Risk indicators (e.g., SOE adjacency, sanctioned adjacency)
- Geolocation (latitude and longitude)
- Real-time temperature at entity location

## Notes
- The Sayari API token is retrieved securely using the internal token_manager.
- The script includes basic error handling and logs when entities or data are not found.
- This project is intended as a sample PoC and can be easily extended for production use.