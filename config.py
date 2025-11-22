"""
Configuration settings for the Google Rank Tracking System
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SerpAPI Configuration
SERPAPI_KEY = os.getenv('SERPAPI_KEY')
SERPAPI_URL = 'https://serpapi.com/search.json'

# Google Sheets Configuration (optional)
GOOGLE_SHEETS_CREDENTIALS_FILE = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE', 'credentials.json')
GOOGLE_SHEETS_SPREADSHEET_ID = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')

# Google Docs Configuration
GOOGLE_DOCS_DOCUMENT_ID = os.getenv('GOOGLE_DOCS_DOCUMENT_ID')

# Search Configuration
MAX_RESULTS_TO_CHECK = 100  # Check top 100 results (10 pages)
RESULTS_PER_PAGE = 10

# Output Configuration
STORAGE_TYPE = os.getenv('STORAGE_TYPE', 'docs').lower()  # Options: 'docs' or 'sheets'
USE_GOOGLE_SHEETS = (STORAGE_TYPE == 'sheets')  # For backward compatibility

