# src/fetch_xlsx.py
import pandas as pd
from src.util import find_files, download_file
import logging

def fetch_xlsx_data(drive, subfolder_id):
    """Fetches the Excel file from Google Drive and processes it into a DataFrame."""
    
    logging.info(f"Searching for Excel file in folder ID: {subfolder_id}")
    # Step 1: Find Excel files in the specified folder
    excel_files = find_files(drive, f"'{subfolder_id}' in parents and mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'")
    
    if not excel_files:
        logging.error("Excel file not found in the specified folder.")
        raise FileNotFoundError("Excel file not found in the specified folder.")
    
    excel_file_id = excel_files[0]['id']
    logging.info(f"Excel file found: '{excel_files[0]['name']}' (ID: {excel_file_id})")

    # Step 2: Download the Excel file content
    try:
        logging.info(f"Downloading Excel file ID: {excel_file_id}")
        excel_content = download_file(drive, excel_file_id)
    except Exception as e:
        logging.error(f"Failed to download Excel file ID {excel_file_id}: {e}")
        raise
    
    # Step 3: Read the Excel content into a DataFrame and process the 'Date' column
    try:
        logging.info("Reading Excel content into a DataFrame.")
        schedule_df = pd.read_excel(excel_content, engine='openpyxl')
        
        if 'Date' not in schedule_df.columns:
            logging.error("The 'Date' column is missing in the Excel file.")
            raise ValueError("The 'Date' column is missing in the Excel file.")
        
        logging.info("Converting 'Date' column to datetime format.")
        schedule_df['Date'] = pd.to_datetime(schedule_df['Date'], format='%m/%d/%Y', errors='coerce')
        
        if schedule_df['Date'].isnull().any():
            logging.warning("Some 'Date' values could not be converted and have been set to NaT.")
        
        return schedule_df
    
    except Exception as e:
        logging.error(f"Error processing Excel content: {e}")
        raise