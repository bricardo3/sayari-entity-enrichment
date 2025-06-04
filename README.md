# Sayari Entity Enrichment

This is a small project I built to demonstrate how to enrich entity profiles using the Sayari API, along with some external data like geolocation and real-time weather. It's meant to simulate a real-world scenario that a Solutions Engineer might face during a client engagement.

## Project Structure

- `sayari/`: Functions to authenticate and query the Sayari API
- `utils/`: Helpers for file reading, weather lookup, and entity details
- `src/main.py`: Main script that ties everything together — from reading the Excel file to exporting enriched results

## Requirements

- Python 3.10+
- All required libraries are listed in `requirements.txt`

## How to Run

1. Clone or download this repo  
2. Install the dependencies:
   pip install -r requirements.txt
3. Run the script:
python src/main.py
4. Select your input Excel file when the file dialog opens
5. Once it's done, you'll be asked where to save the output

## Input File Format
Your Excel file should have at least one sheet that includes these three columns (case-insensitive):
- name
- address
- country (use the 3-letter ISO code like RUS, CHN, USA, etc.)

## Output
The output is another Excel file with your original data plus new columns, including:
- Sayari entity ID
- Sanctions status
- Export control flags and levels
- Related entities count
- Risk indicators 
- Geolocation (latitude and longitude)
- Current temperature at entity location

## Notes
- The Sayari token is fetched automatically (just make sure your credentials are set as environment variables).
- I added basic error handling to skip missing or incomplete entries without breaking the process.
- This is a proof of concept, but the code can be adapted for more advanced use cases or even production if needed.