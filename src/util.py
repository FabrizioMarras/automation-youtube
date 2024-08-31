# src/util.py
import io
from googleapiclient.http import MediaIoBaseDownload
from pytz import timezone
from datetime import datetime

# Find Files ---------------------------------------------------------------
def find_files(drive, query):
    response = drive.files().list(q=query, spaces='drive', fields='nextPageToken, files(id, name)').execute()
    return response.get('files', [])

# Download Files -----------------------------------------------------------
def download_file(drive, file_id):
    request = drive.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh

# Convert Date --------------------------------------------------------------
def convert_date(date, hour=17, minute=0, second=0):
    # Set the CET timezone
    cet = timezone('CET')
    utc = timezone('UTC')
    dt = datetime(date.year, date.month, date.day, hour, minute, second)

    # Localize the datetime to CET, considering DST
    cet_time = cet.localize(dt)
    
    # Convert CET time to UTC
    utc_time = cet_time.astimezone(utc)
    
    return utc_time.isoformat()
