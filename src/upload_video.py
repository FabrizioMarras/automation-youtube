import os
from googleapiclient.http import MediaFileUpload
import logging

def upload_video(youtube, video_file_path, title, description, scheduled_time):
    """Uploads a video to YouTube and schedules it for a specified time.
    
    Parameters:
        youtube: Authenticated YouTube API client.
        video_file_path (str): Path to the video file to be uploaded.
        title (str): Title of the video.
        description (str): Description of the video.
        scheduled_time (str): Scheduled publish time in ISO 8601 format.

    Returns:
        dict: The response from the YouTube API if successful, None otherwise.
    """
    try:
        logging.info(f"Preparing to upload video '{video_file_path}' with title '{title}'.")

        body = {
            'snippet': {
                'title': title,
                'description': description,
                'categoryId': '22',  # Category ID for 'People & Blogs'
            },
            'status': {
                'privacyStatus': 'private',
                'publishAt': scheduled_time,
                'selfDeclaredMadeForKids': False,
            }
        }

        # Use the path to the temporary file to upload to YouTube
        media = MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )

        # Handle resumable upload and wait for completion
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                logging.info(f"Upload progress: {progress}%")

        if response:
            video_id = response["id"]
            logging.info(f"Video ID {video_id} has been uploaded and scheduled to go live at {scheduled_time}.")
            return response
        else:
            logging.warning("Upload completed but no response was returned.")
            return None

    except Exception as e:
        logging.error(f"An error occurred during video upload: {e}")
        return None

    finally:
        # Ensure the temporary video file is removed after the upload attempt
        try:
            os.remove(video_file_path)
            logging.info(f"Temporary video file '{video_file_path}' has been removed.")
        except OSError as e:
            logging.warning(f"Failed to remove temporary video file '{video_file_path}': {e}")
