import os
from googleapiclient.http import MediaFileUpload

def upload_video(youtube, video_file_path, title, description, scheduled_time):
    try:
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
                print(f"Upload progress: {int(status.progress() * 100)}%")

        print(f'Video ID {response["id"]} has been uploaded and scheduled to go live at {scheduled_time}')
        return response
    finally:
        # Clean up the temporary file after the upload
        os.remove(video_file_path)
