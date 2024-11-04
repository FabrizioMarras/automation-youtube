# YouTube Video Scheduler

This Python application automates the process of uploading and scheduling videos to YouTube using data stored in Google Drive. The videos and metadata (content, tags, etc.) are retrieved from specific folders in Google Drive based on the information provided in an Excel file.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Known Issues](#known-issues)
- [Future Improvements](#future-improvements)
- [License](#license)

## Features
- Fetch video metadata from an Excel file stored in Google Drive.
- Download video files from Google Drive.
- Upload and schedule videos on YouTube.
- Automatically handle time zones and daylight saving time for scheduled uploads.

## Prerequisites
- Python 3.7 or higher
- Google Cloud Project with YouTube Data API and Google Drive API enabled.
- Service account credentials (JSON key file) from Google for authentication.

## Installation

### 1. Install Python
Ensure you have Python 3.7 or higher installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).

### 2. Clone the Repository
Clone this repository to your local machine using:

```bash
git clone https://github.com/yourusername/youtube-video-scheduler.git
cd youtube-video-scheduler
```

### 3. Set Up a Virtual Environment
Set up a virtual environment to manage dependencies:

```bash
python3 -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

### 4. Install Required Dependencies
Install the required Python packages using:

```bash
pip install -r requirements.txt
```

### 5. Set Up Service Account Credentials
Obtain the `service_account_key.json` credentials file from Google Cloud Console.
Place this file in the root directory of the project.
If not sure how to do it, please follow Google documentation.

### 6. Configure .gitignore
Make sure your .gitignore file includes entries to exclude virtual environments, API credentials, and other unnecessary files:

```bash
.env
env/
__pycache__/
service_account_key.json
```


## Usage

### 1. Prepare the Excel File

- Select one of the folders in your Google Drive as main folder for this project.
- Create a subfolder containing the Excel file with all the information about the videos and metadata (content, tags, etc.).
- Save the main folder ID and subfolder name in your `.env` file:

```bash
MAIN_FOLDER_ID='your_google_drive_folder_ID'
SUBFOLDER_NAME='your_subfolder_name'
```

- The Excel file must contain the following columns:
    - No: The number associated with the video file name.
    - Date: The date to schedule the post (time will be set to 5:00 PM CET by default).
    - Test: The test name associated with the video.
    - Name: The type of test (e.g., Watch, Follow).
    - Char: The character name.
    - AInsyte Message: The content of the post.
    - Hash #: Hashtags for the post (multiple columns).

- The Videos should follow the structure:
    - Parent folder with name containing the "Test" name associated with the video.
    - Child folder with name containing the "No" associated with the video file name.
    - Video contained inside child folder with name `Post {No}.mp4`.

### 2. Run the Application
Execute the main script to start the process:

```bash
python3 main.py
```

This will:
- Authenticate with Google using Service Account Credentials.
- Fetch and parse the Excel file.
- Download the relevant video files and Post content from Google Drive.
- Upload and schedule the videos on YouTube.

### 3. Quota Management
YouTube API has a daily quota limit. The script is designed to handle uploads within these limits. If you need to upload more than the allowed quota, consider spreading the uploads over multiple days or requesting an increase in quota from Google.

## Project Structure

```
youtube-video-scheduler/
│
├── service_account_key.json                    # Authentication credentials (not included in the repo)
├── env/                                        # Virtual environment (excluded from version control)
├── main.py                                     # Main script
├── requirements.txt                            # List of Python dependencies
├── .gitignore                                  # Git ignore file
├── .env                                        # env file (not included)
├── README.md                                   # This file
└── src/                                        # Source files
    ├── auth.py                                 # Authentication with Google services
    ├── config.py                               # Configuration class to load API keys, tokens, and other variables from .env file.
    ├── fetch_xlsx.py                           # Functions to fetch and parse the Excel file
    ├── fetch_video.py                          # Functions to download video files from Google Drive
    ├── upload_video.py                         # Functions to upload and schedule videos on YouTube
    └── util.py                                 # Utility functions (date conversion, file download, etc.)
```

## Known Issues
- The YouTube API quota may limit the number of videos that can be uploaded per day.

## Future Improvements
- Add a retry mechanism for uploads that fail due to quota limits.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

