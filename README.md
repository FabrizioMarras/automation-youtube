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
- OAuth 2.0 credentials (client secret JSON file) from Google for authentication.

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

### 5. Set Up OAuth 2.0 Credentials
Obtain the `credentials-youtube-posts-automation.json` credentials file from Google Cloud Console.
Place this file in the root directory of the project.

### 6. Configure .gitignore
Make sure your .gitignore file includes entries to exclude virtual environments, API credentials, and other unnecessary files:

```bash
env/
__pycache__/
credentials-youtube-posts-automation.json
```

## Usage

### 1. Prepare the Excel File
- The Excel file should be stored in a specific folder within Google Drive.
- The Excel file must contain the following columns:
    - No: The number associated with the video file name.
    - Date: The date to schedule the post (time will be set to 5:00 PM CET).
    - Test: The test name associated with the video.
    - Name: The type of test (e.g., Watch, Follow).
    - Char: The character name.
    - AInsyte Message: The content of the post.
    - Hash #: Hashtags for the post (multiple columns).

### 2. Run the Application
Execute the main script to start the process:

```bash
python3 main.py
```

This will:
- Authenticate with Google using OAuth 2.0.
- Fetch and parse the Excel file.
- Download the relevant video files from Google Drive.
- Upload and schedule the videos on YouTube.

### 3. Quota Management
YouTube API has a daily quota limit. The script is designed to handle uploads within these limits. If you need to upload more than the allowed quota, consider spreading the uploads over multiple days or requesting an increase in quota from Google.

## Project Structure

```
youtube-video-scheduler/
│
├── credentials-youtube-posts-automation.json   # OAuth 2.0 credentials (not included in the repo)
├── env/                                        # Virtual environment (excluded from version control)
├── main.py                                     # Main script
├── requirements.txt                            # List of Python dependencies
├── .gitignore                                  # Git ignore file
├── README.md                                   # This file
└── src/                                        # Source files
    ├── auth.py                                 # Authentication with Google services
    ├── fetch_xlsx.py                           # Functions to fetch and parse the Excel file
    ├── fetch_video.py                          # Functions to download video files from Google Drive
    ├── upload_video.py                         # Functions to upload and schedule videos on YouTube
    └── util.py                                 # Utility functions (date conversion, file download, etc.)
```

## Known Issues
- The script currently requires manual authentication with Google through a browser.
- The YouTube API quota may limit the number of videos that can be uploaded per day.

## Future Improvements
- Implement automated re-authentication to remove the manual OAuth 2.0 process.
- Add a retry mechanism for uploads that fail due to quota limits.
- Improve logging and error handling to better track the upload process.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
