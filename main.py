# main.py
import os
import pandas as pd
import logging
from dotenv import load_dotenv

from src.auth import get_google_services
from src.fetch_xlsx import fetch_xlsx_data
from src.fetch_video import fetch_video
from src.util import find_files, convert_date
from src.upload_video import upload_video


# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    # Authenticate Google services (YouTube and Drive)
    try:
        youtube, drive = get_google_services()
        logging.info("Successfully authenticated Google services.")
    except Exception as e:
        logging.error(f"Failed to authenticate Google services: {e}")
        return

    # Fetch the main folder ID and subfolder name from environment variables
    main_folder_id = os.getenv('MAIN_FOLDER_ID')
    subfolder_name = os.getenv('SUBFOLDER_NAME')
    if not main_folder_id or not subfolder_name:
        logging.error("MAIN_FOLDER_ID or SUBFOLDER_NAME is not set in the environment variables.")
        return
    
    # Locate the character folder
    logging.info(f"Searching for subfolder '{subfolder_name}' in main folder ID '{main_folder_id}'.")
    subfolders = find_files(drive, f"name='{subfolder_name}' and '{main_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'")
    if not subfolders:
        logging.warning(f"Subfolder '{subfolder_name}' not found. Exiting.")
        return

    subfolder_id = subfolders[0]['id']
    logging.info(f"Subfolder '{subfolder_name}' found (ID: {subfolder_id}).")

    # Fetch the Excel data
    try:
        schedule_df = fetch_xlsx_data(drive, subfolder_id)
        logging.info("Excel data fetched successfully.")
    except FileNotFoundError as e:
        logging.error(f"Failed to fetch Excel data: {e}")
        return
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching Excel data: {e}")
        return

     # Iterate through rows in the DataFrame
    for index, row in schedule_df.iterrows():
        video_no = row.get('No')
        test_name = row.get('Test')
        test_type = row.get('Name')
        char_name = row.get('Char')
        cell_date = row.get('Date')
        content = row.get('AInsyte Message')
        tags = " ".join([row.get(col, '') for col in schedule_df.columns if "hash" in col.lower() and pd.notna(row.get(col))])

        # Check for missing or empty essential data
        if not all([video_no, test_name, test_type, char_name, content]):
            logging.warning(f"Missing essential data for video number '{video_no}'. Skipping entry.")
            continue

        # Fetch the video file
        try:
            video_file = fetch_video(drive, subfolder_id, test_name, video_no)
            logging.info(f"Downloaded video file for video number '{video_no}'.")
        except FileNotFoundError as e:
            logging.warning(f"Video file not found for video number '{video_no}': {e}. Skipping.")
            continue
        except Exception as e:
            logging.error(f"An unexpected error occurred while fetching video file for video number '{video_no}': {e}. Skipping.")
            continue

        # set date and time for the post
        time = 17
        date = convert_date(cell_date, hour=time, minute=0, second=0, iso_format=True)
        logging.info(f"The post is scheduled for {date}.")

        # set the post content
        post = f'{content} {tags}'

        # create the title of the post in function of the test_type label
        if test_type in ['Watch', 'Follow']:
            title = f'AInsyte - {char_name} - What to {test_type}'
        else:
            title = f'AInsyte decodes {char_name} - {test_name} {test_type}'

        # Log the final output for verification
        logging.info(f"Preparing to upload video number '{video_no}' - Title: '{title}', Scheduled On: '{date}', Post Content: '{post}'")

        # Upload the video to YouTube
        try:
            upload_video(youtube, video_file, title, post, date)
            logging.info(f"Uploaded and scheduled video number '{video_no}' for {date}.")
        except Exception as e:
            logging.error(f"Failed to upload video number '{video_no}': {e}")

if __name__ == '__main__':
    main()
