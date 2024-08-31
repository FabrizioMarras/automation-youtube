# main.py
from src.auth import get_authenticated_service
from src.fetch_xlsx import fetch_xlsx_data
from src.fetch_video import fetch_video
from src.util import find_files, convert_date
from src.upload_video import upload_video
from pytz import timezone
import pandas as pd

def main():
    youtube, drive = get_authenticated_service()
    cet = timezone('CET')
    utc = timezone('UTC')

    main_folder_id = '15-XLoeY65jSyh6sXlhinrs3r1srf0lyp'
    subfolder_name = 'Harry Potter (HP)'
    
    # Locate the character folder
    subfolders = find_files(drive, f"name='{subfolder_name}' and '{main_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'")
    if not subfolders:
        print(f"{subfolder_name} folder not found")
        return

    subfolder_id = subfolders[0]['id']

    # Fetch the Excel data
    schedule_df = fetch_xlsx_data(drive, subfolder_id)

    for index, row in schedule_df.iterrows():
        video_no = row['No']
        test_name = row['Test']
        test_type = row['Name']
        char_name = row['Char']
        cell_date = row['Date']
        content = row['AInsyte Message']
        tags = " ".join([row[col] for col in schedule_df.columns if "hash" in col.lower() and pd.notna(row[col])])

        # Fetch the video file
        try:
            video_file = fetch_video(drive, subfolder_id, test_name, video_no)
            print(f"Downloaded video file for {video_no}")
        except FileNotFoundError as e:
            print(e)
            continue

        # set date and time for the post
        time = 17
        date = convert_date(cell_date, hour=time)
        print(f"The post is scheduled for {date}")

        # set the post content
        post = f'{content} {tags}'

        # create the title of the post in function of the test_type label
        if test_type in ['Watch', 'Follow']:
            title = f'AInsyte - {char_name} - What to {test_type}'
        else:
            title = f'AInsyte decodes {char_name} - {test_name} {test_type}'

        # Print the final output for verification
        print('video: ', video_no, 'test: ', test_name, 'Scheduled On: ', date, 'Title: ', title, 'Post: ', post)

        # Upload the video to YouTube
        try:
            upload_video(youtube, video_file, title, post, date)
            print(f"Uploaded and scheduled video: {video_no} for {date}")
        except Exception as e:
            print(f"Failed to upload video {video_no}: {e}")

if __name__ == '__main__':
    main()
