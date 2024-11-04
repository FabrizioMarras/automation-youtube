# src/util.py
import io
from googleapiclient.http import MediaIoBaseDownload
from pytz import timezone
from datetime import datetime, date as date_type
from typing import Union
import logging

# Find Files ---------------------------------------------------------------
def find_files(drive, query):
    """Find files in Google Drive based on a query."""
    try:
        response = drive.files().list(q=query, spaces='drive', fields='nextPageToken, files(id, name)').execute()
        files = response.get('files', [])
        logging.info(f"Found {len(files)} files matching query: {query}")
        return files
    except Exception as e:
        logging.error(f"Error finding files with query '{query}': {e}")
        raise

# Download Files -----------------------------------------------------------
def download_file(drive, file_id):
    """Download a file from Google Drive."""
    try:
        request = drive.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            logging.info(f"Download progress: {int(status.progress() * 100)}%")
        fh.seek(0)
        logging.info(f"File {file_id} downloaded successfully.")
        return fh
    except Exception as e:
        logging.error(f"Error downloading file with ID {file_id}: {e}")
        raise

# Convert Date --------------------------------------------------------------
def convert_date(
    date: date_type,
    hour: int = 17,
    minute: int = 0,
    second: int = 0,
    iso_format: bool = False
) -> Union[str, datetime]:
    """
    Convert a date to a specific time, localized to UTC or CET.
    
    Parameters:
        date: date object (input date)
        hour: int (hour to set, default is 17)
        minute: int (minute to set, default is 0)
        second: int (second to set, default is 0)
        iso_format: bool (if True, return ISO formatted string, if False, return UTC datetime object)
  
    Returns:
        A datetime object or ISO formatted string based on `iso_format` flag.
    """
    try:
        # Define timezones
        cet = timezone('CET')  # Central European Time
        utc = timezone('UTC')  # Universal Time Coordinates (UTC)
        
        # Create the datetime object for the provided date, time, and CET timezone
        dt = datetime(date.year, date.month, date.day, hour, minute, second)
        cet_time = cet.localize(dt)
        
        # Convert to UTC
        utc_time = cet_time.astimezone(utc)
        
        # Return ISO formatted string if requested, otherwise return datetime object
        return utc_time.isoformat() if iso_format else utc_time
    except Exception as e:
        raise ValueError(f"Error converting date: {e}")

