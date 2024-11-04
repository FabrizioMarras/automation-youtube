from src.util import find_files, download_file
import tempfile
import logging

def fetch_video(drive, subfolder_id, test_name, video_no):
    """Download the video file from Google Drive."""
    # Step 1: Find the test folder within the character folder
    logging.info(f"Searching for test folder: '{test_name}' under subfolder ID: {subfolder_id}")
    test_folders = find_files(drive, f"name contains '{test_name}' and '{subfolder_id}' in parents and mimeType='application/vnd.google-apps.folder'")
    
    if not test_folders:
        logging.error(f"Test folder containing '{test_name}' not found")
        raise FileNotFoundError(f"Test folder containing '{test_name}' not found")

    test_folder_id = test_folders[0]['id']
    logging.info(f"Test folder found: '{test_folders[0]['name']}' (ID: {test_folder_id})")

    # Step 2: Find the video folder inside the test folder
    logging.info(f"Searching for video folder containing video number '{video_no}' under test folder ID: {test_folder_id}")
    video_folders = find_files(drive, f"name contains '{video_no}' and '{test_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'")
    
    if not video_folders:
        logging.error(f"Folder for video number '{video_no}' not found under test '{test_name}'")
        raise FileNotFoundError(f"Folder for video number '{video_no}' not found under test '{test_name}'")

    video_folder_id = video_folders[0]['id']
    logging.info(f"Video folder found: '{video_folders[0]['name']}' (ID: {video_folder_id})")

    # Step 3: Find the video file inside the video folder
    video_file_name = f"Post {video_no}.mp4"
    logging.info(f"Searching for video file: '{video_file_name}' in folder ID: {video_folder_id}")
    videos = find_files(drive, f"name = '{video_file_name}' and '{video_folder_id}' in parents")
    
    if not videos:
        logging.error(f"Video file '{video_file_name}' not found")
        raise FileNotFoundError(f"Video file '{video_file_name}' not found")

    video_file_id = videos[0]['id']
    logging.info(f"Video file found: '{videos[0]['name']}' (ID: {video_file_id})")

    # Step 4: Download the video file to a temporary location
    logging.info(f"Downloading video file ID: {video_file_id}")
    try:
        video_file = download_file(drive, video_file_id)
        temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_video_file.write(video_file.read())
        temp_video_file.close()
        logging.info(f"Video downloaded to temporary file: {temp_video_file.name}")
        return temp_video_file.name
    except Exception as e:
        logging.error(f"Failed to download video file ID {video_file_id}: {e}")
        raise
