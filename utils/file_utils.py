import pandas as pd

REQUIRED_COLUMNS = {"name", "address", "country"}

def extract_entities_from_excel(file_path: str):
    try:
        xl = pd.ExcelFile(file_path)
    except Exception as e:
        raise ValueError(f"Failed to read Excel file: {str(e)}")

    entries = []

    for sheet_name in xl.sheet_names:
        try:
            df = xl.parse(sheet_name)
        except Exception as e:
            print(f"⚠️ Skipping sheet '{sheet_name}' due to error: {str(e)}")
            continue

        if df.empty:
            print(f"⚠️ Skipping empty sheet: {sheet_name}")
            continue

        # Normalize columns
        df.columns = [col.strip().lower() for col in df.columns]
        if not REQUIRED_COLUMNS.issubset(df.columns):
            print(f"⚠️ Sheet '{sheet_name}' missing required columns. Skipping.")
            continue

        for idx, row in df.iterrows():
            name = str(row.get("name", "")).strip()
            address = str(row.get("address", "")).strip()
            country = str(row.get("country", "")).strip()

            if not name and not address:
                continue  # Skip rows with no useful data

            entries.append({
                "sheet": sheet_name,
                "row": idx + 2,  # +2 because pandas is 0-indexed and we skip header
                "name": name,
                "address": address,
                "country": country
            })

    if not entries:
        raise ValueError("No valid data rows found in any sheet.")

    return entries
