from src.util import find_files, download_file
import tempfile

def fetch_video(drive, subfolder_id, test_name, video_no):
    # Find the test folder within the character folder
    test_folders = find_files(drive, f"name contains '{test_name}' and '{subfolder_id}' in parents and mimeType='application/vnd.google-apps.folder'")
    if not test_folders:
        raise FileNotFoundError(f"Test folder containing '{test_name}' not found")

    test_folder_id = test_folders[0]['id']

    # Find the video folder inside the test folder
    video_folders = find_files(drive, f"name contains '{video_no}' and '{test_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'")
    if not video_folders:
        raise FileNotFoundError(f"Folder for video No '{video_no}' not found under test '{test_name}'")

    video_folder_id = video_folders[0]['id']

    # Find the video file inside the video folder
    videos = find_files(drive, f"name contains 'Post {video_no}.mp4' and '{video_folder_id}' in parents")
    if not videos:
        raise FileNotFoundError(f"Video file 'Post {video_no}.mp4' not found")

    video_file_id = videos[0]['id']

    # Download the video file to a temporary location
    video_file = download_file(drive, video_file_id)
    temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video_file.write(video_file.read())
    temp_video_file.close()

    return temp_video_file.name
