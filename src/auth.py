from google.oauth2 import service_account
from googleapiclient.discovery import build
from src.config import Config

def get_google_services():
    """
    Authenticates and returns both Google Drive and YouTube service objects.

    Returns:
        A tuple of YouTube and Google Drive service objects.
    """
    SCOPES = [
        'https://www.googleapis.com/auth/youtube.force-ssl',
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = service_account.Credentials.from_service_account_file(
        Config.SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    # If using domain-wide delegation, specify the user to impersonate
    credentials = credentials.with_subject(Config.DELEGATED_USER_EMAIL)

    # Build the service objects for YouTube and Google Drive
    youtube = build('youtube', 'v3', credentials=credentials)
    drive = build('drive', 'v3', credentials=credentials)

    return youtube, drive