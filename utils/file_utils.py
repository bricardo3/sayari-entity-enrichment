import pandas as pd

REQUIRED_COLUMNS = {"name", "address", "country"}

def extract_entities_from_excel(file_path: str):
    try:
        xl = pd.ExcelFile(file_path)
    except Exception as e:
        raise ValueError(f"Couldn’t open the Excel file: {e}")

    entries = []

    for sheet_name in xl.sheet_names:
        try:
            df = xl.parse(sheet_name)
        except Exception as e:
            print(f"Skipping sheet '{sheet_name}' (error reading it): {e}")
            continue

        if df.empty:
            print(f"Sheet '{sheet_name}' is empty. Skipping.")
            continue

        # Lowercase and strip column names
        df.columns = [col.strip().lower() for col in df.columns]

        if not REQUIRED_COLUMNS.issubset(df.columns):
            print(f"Sheet '{sheet_name}' is missing required columns.")
            continue

        for idx, row in df.iterrows():
            name = str(row.get("name", "")).strip()
            address = str(row.get("address", "")).strip()
            country = str(row.get("country", "")).strip()

            if not name and not address:
                continue  # skip incomplete row

            entries.append({
                "sheet": sheet_name,
                "row": idx + 2,  # +2 for header and zero-indexing
                "name": name,
                "address": address,
                "country": country
            })

    if not entries:
        raise ValueError("No usable rows found in the Excel file.")

    return entries
