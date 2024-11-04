import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class to load API keys, tokens, and other variables from .env file."""

    # Google API (YouTube and Drive)
    SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
    DELEGATED_USER_EMAIL = os.getenv('DELEGATED_USER_EMAIL')

    # Main Folder ID for Google Drive
    MAIN_FOLDER_ID = os.getenv('MAIN_FOLDER_ID')

    @staticmethod
    def check_required_vars():
        """Checks that all required environment variables are loaded."""
        required_vars = [
            'SERVICE_ACCOUNT_FILE', 'DELEGATED_USER_EMAIL', 'MAIN_FOLDER_ID'
        ]

        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Call this function at the start of your application to ensure all variables are loaded
Config.check_required_vars()
