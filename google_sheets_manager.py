"""
Google Sheets Manager Module
Handles reading from and writing to Google Sheets
"""
import os
from typing import List, Dict, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle
import config


class GoogleSheetsManager:
    """Manages Google Sheets operations for storing ranking data"""
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    def __init__(self, credentials_file: str = None, spreadsheet_id: str = None):
        """
        Initialize Google Sheets Manager
        
        Args:
            credentials_file: Path to Google OAuth credentials JSON file
            spreadsheet_id: Google Sheets spreadsheet ID
        """
        self.credentials_file = credentials_file or config.GOOGLE_SHEETS_CREDENTIALS_FILE
        self.spreadsheet_id = spreadsheet_id or config.GOOGLE_SHEETS_SPREADSHEET_ID
        
        if not self.spreadsheet_id:
            raise ValueError("Google Sheets Spreadsheet ID is required. Set GOOGLE_SHEETS_SPREADSHEET_ID in .env file")
        
        self.service = self._authenticate()
    
    def _authenticate(self):
        """Authenticate and return Google Sheets service"""
        creds = None
        token_file = 'token.pickle'
        
        # Load existing token
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_file}\n"
                        "Please download OAuth 2.0 credentials from Google Cloud Console"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        return build('sheets', 'v4', credentials=creds)
    
    def create_sheet_if_not_exists(self, sheet_name: str = "Rank Tracking"):
        """
        Create a new sheet if it doesn't exist
        
        Args:
            sheet_name: Name of the sheet to create
        """
        try:
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            sheet_names = [sheet['properties']['title'] for sheet in spreadsheet.get('sheets', [])]
            
            if sheet_name not in sheet_names:
                # Create new sheet
                body = {
                    'requests': [{
                        'addSheet': {
                            'properties': {
                                'title': sheet_name
                            }
                        }
                    }]
                }
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body=body
                ).execute()
                print(f"Created new sheet: {sheet_name}")
        except HttpError as error:
            print(f"Error creating sheet: {error}")
    
    def initialize_headers(self, sheet_name: str = "Rank Tracking"):
        """
        Initialize headers in the sheet if not already present
        
        Args:
            sheet_name: Name of the sheet
        """
        headers = ['Keyword', 'Website URL', 'Ranking Position', 'Found URL', 
                  'Checked On', 'SERP Title', 'SERP Snippet', 'Notes']
        
        try:
            # Check if headers exist
            range_name = f"{sheet_name}!A1:H1"
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            
            if not values or values[0] != headers:
                # Write headers
                body = {
                    'values': [headers]
                }
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=range_name,
                    valueInputOption='RAW',
                    body=body
                ).execute()
                print("Headers initialized")
        except HttpError as error:
            print(f"Error initializing headers: {error}")
    
    def append_results(self, results: List[Dict], sheet_name: str = "Rank Tracking"):
        """
        Append ranking results to Google Sheets
        
        Args:
            results: List of ranking result dictionaries
            sheet_name: Name of the sheet to write to
        """
        if not results:
            return
        
        # Ensure sheet exists
        self.create_sheet_if_not_exists(sheet_name)
        
        # Initialize headers if needed
        self.initialize_headers(sheet_name)
        
        # Prepare data rows
        values = []
        for result in results:
            row = [
                result.get('keyword', ''),
                result.get('website_url', ''),
                str(result.get('ranking_position', '')),
                result.get('found_url', ''),
                result.get('checked_on', ''),
                result.get('serp_title', ''),
                result.get('serp_snippet', ''),
                result.get('error', '') or ''
            ]
            values.append(row)
        
        # Append to sheet
        try:
            range_name = f"{sheet_name}!A2"
            body = {
                'values': values
            }
            
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            print(f"Successfully appended {len(results)} results to {sheet_name}")
        except HttpError as error:
            print(f"Error appending results: {error}")
    
    def get_all_results(self, sheet_name: str = "Rank Tracking") -> List[List]:
        """
        Get all results from the sheet
        
        Args:
            sheet_name: Name of the sheet
            
        Returns:
            List of rows from the sheet
        """
        try:
            range_name = f"{sheet_name}!A:H"
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            return result.get('values', [])
        except HttpError as error:
            print(f"Error reading results: {error}")
            return []


