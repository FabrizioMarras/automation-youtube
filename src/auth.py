# youtube_auth.py
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def get_authenticated_service():
    CLIENT_SECRETS_FILE = "credentials-youtube-posts-automation.json"
    SCOPES = [
        'https://www.googleapis.com/auth/youtube.force-ssl', 
        'https://www.googleapis.com/auth/drive.readonly']

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    youtube = build('youtube', 'v3', credentials=credentials)
    drive = build('drive', 'v3', credentials=credentials)
    return youtube, drive
