import sys
import time
import pandas as pd
from tkinter import Tk, filedialog
from sayari.token_manager import get_token
from sayari.search import search_entity_and_coordinates
from utils.entity_utils import get_entity_details
from utils.file_utils import extract_entities_from_excel
from utils.weather_utils import get_current_temperature
from datetime import datetime

REQUIRED_COLUMNS = {"name", "address", "country"}

def select_file():
    # Abre o diálogo para o usuário escolher o arquivo Excel
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select the Excel file",
        filetypes=[("Excel files", "*.xlsx")]
    )
    return file_path

def validate_file(file_path):
    # Valida se o arquivo é válido e contém os dados esperados
    if not file_path:
        print("No file selected.")
        sys.exit()

    if not file_path.endswith(".xlsx"):
        print("Invalid file type. Please select a .xlsx file.")
        sys.exit()

    try:
        excel_file = pd.ExcelFile(file_path)
    except Exception as e:
        print(f"Could not read the Excel file: {e}")
        sys.exit()

    valid_sheets = []
    for sheet in excel_file.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet)
        df_columns = set(df.columns.str.lower())
        if REQUIRED_COLUMNS.issubset(df_columns):
            if df.empty:
                print(f"Sheet '{sheet}' is empty.")
            else:
                valid_sheets.append(sheet)
        else:
            print(f"Sheet '{sheet}' is missing required columns: {REQUIRED_COLUMNS}")

    if not valid_sheets:
        print("No sheet with the expected structure was found.")
        sys.exit()

    print("File loaded successfully.")
    return excel_file, valid_sheets

def main():
    file_path = select_file()
    excel_file, valid_sheets = validate_file(file_path)

    token = get_token()
    entries = extract_entities_from_excel(file_path)
    enriched_data = []

    for i, entry in enumerate(entries):
        print(f"Looking up entity {i + 1}/{len(entries)}: {entry['name']}")

        entity_id, latitude, longitude = search_entity_and_coordinates(entry, token)

        if not entity_id:
            print(f"No results found for: {entry['name']}")
            enriched_data.append({
                **entry,
                "entity_id": "Not found",
                "translated_name": "Not found",
                "type": "Not found",
                "identifiers": "Not found",
                "sanctioned": "Not found",
                "meu_list_contractors": "Not found",
                "sanctioned_adjacent": "Not found",
                "soe_adjacent": "Not found",
                "export_controls_adjacent": "Not found",
                "degree": "Not found",
                "relationship_count": "Not found",
                "related_entities_count": "Not found",
                "source_count": "Not found",
                "latitude": "Not found",
                "longitude": "Not found",
                "temperature": "Not available"
            })
            continue

        entity_details = get_entity_details(entity_id, token)

        if latitude and longitude:
            temperature = get_current_temperature(latitude, longitude)
        else:
            print("No coordinates available for this entity.")
            temperature = None

        enriched_data.append({
            **entry,
            "entity_id": entity_details.get("entity_id", "Not found"),
            "translated_name": entity_details.get("translated_name", "Not found"),
            "type": entity_details.get("type", "Not found"),
            "identifiers": entity_details.get("identifiers", "Not found"),
            "sanctioned": entity_details.get("sanctioned", "Not found"),
            "meu_list_contractors": entity_details.get("meu_list_contractors", "Not found"),
            "sanctioned_adjacent": entity_details.get("sanctioned_adjacent", "Not found"),
            "soe_adjacent": entity_details.get("soe_adjacent", "Not found"),
            "export_controls_adjacent": entity_details.get("export_controls_adjacent", "Not found"),
            "degree": entity_details.get("degree", "Not found"),
            "relationship_count": entity_details.get("relationship_count", "Not found"),
            "related_entities_count": entity_details.get("related_entities_count", "Not found"),
            "source_count": entity_details.get("source_count", "Not found"),
            "latitude": latitude or "Not found",
            "longitude": longitude or "Not found",
            "temperature": temperature if temperature is not None else "Not available"
        })

        time.sleep(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H-%M-%S")
    default_filename = f"sayari_output_{timestamp}.xlsx"

    df_output = pd.DataFrame(enriched_data)

    output_path = filedialog.asksaveasfilename(
        title="Save Enriched Excel File",
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        initialfile=default_filename
    )

    if output_path:
        df_output.to_excel(output_path, index=False)
        print(f"File saved at: {output_path}")
    else:
        print("Save canceled.")

if __name__ == "__main__":
    main()
