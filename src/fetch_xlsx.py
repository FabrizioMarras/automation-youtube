# src/fetch_xlsx.py
import pandas as pd
from src.util import find_files, download_file

def fetch_xlsx_data(drive, subfolder_id):
    excel_files = find_files(drive, f"'{subfolder_id}' in parents and mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'")
    if not excel_files:
        raise FileNotFoundError("Excel file not found in character folder")

    excel_file_id = excel_files[0]['id']
    excel_content = download_file(drive, excel_file_id)
    
    # Read the Excel file and process the dates
    schedule_df = pd.read_excel(excel_content, engine='openpyxl')
    schedule_df['Date'] = pd.to_datetime(schedule_df['Date'], format='%m/%d/%Y', errors='coerce')
    
    return schedule_df
