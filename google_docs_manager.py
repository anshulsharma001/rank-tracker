"""
Google Docs Manager Module
Handles reading from and writing to Google Docs
"""
import os
from typing import List, Dict, Optional
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle
import config


class GoogleDocsManager:
    """Manages Google Docs operations for storing ranking data"""
    
    SCOPES = ['https://www.googleapis.com/auth/documents']
    
    def __init__(self, credentials_file: str = None, document_id: str = None):
        """
        Initialize Google Docs Manager
        
        Args:
            credentials_file: Path to Google OAuth credentials JSON file
            document_id: Google Docs document ID
        """
        self.credentials_file = credentials_file or config.GOOGLE_SHEETS_CREDENTIALS_FILE
        self.document_id = document_id or config.GOOGLE_DOCS_DOCUMENT_ID
        
        if not self.document_id:
            raise ValueError("Google Docs Document ID is required. Set GOOGLE_DOCS_DOCUMENT_ID in .env file")
        
        self.service = self._authenticate()
    
    def _authenticate(self):
        """Authenticate and return Google Docs service"""
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
        
        return build('docs', 'v1', credentials=creds)
    
    def _ensure_headers(self):
        """Ensure headers exist in the document"""
        try:
            doc = self.service.documents().get(documentId=self.document_id).execute()
            content = doc.get('body', {}).get('content', [])
            
            # Extract text from document to check if it's empty
            text = ""
            for element in content:
                if 'paragraph' in element:
                    for para_element in element['paragraph'].get('elements', []):
                        if 'textRun' in para_element:
                            text += para_element['textRun'].get('content', '')
            
            # Check if document is empty or doesn't have headers
            if not text.strip():
                # Create headers at index 1 (right after document start)
                requests = [{
                    'insertText': {
                        'location': {'index': 1},
                        'text': 'Keyword\tWebsite URL\tRanking Position\tFound URL\tChecked On\tSERP Title\tSERP Snippet\tNotes\n'
                    }
                }]
                self.service.documents().batchUpdate(
                    documentId=self.document_id,
                    body={'requests': requests}
                ).execute()
                print("Headers initialized in Google Docs")
        except HttpError as error:
            print(f"Error ensuring headers: {error}")
    
    def append_results(self, results: List[Dict], document_name: str = None):
        """
        Append ranking results to Google Docs
        
        Args:
            results: List of ranking result dictionaries
            document_name: Not used (kept for compatibility)
        """
        if not results:
            return
        
        try:
            # Ensure headers exist
            self._ensure_headers()
            
            # Get document to find end index
            doc = self.service.documents().get(documentId=self.document_id).execute()
            content = doc.get('body', {}).get('content', [])
            
            # Find the end of the document
            # Google Docs indices: 1 = start, endIndex is exclusive, so insert at endIndex-1
            end_index = 1
            if content:
                # Get the last element's end index
                for element in reversed(content):
                    if 'endIndex' in element:
                        end_index = element['endIndex']
                        break
            
            # If end_index is 2 or less (empty doc with just paragraph structure), use 1
            # Otherwise, we need to insert before the end, so use end_index - 1
            if end_index <= 2:
                insert_index = 1
            else:
                # Insert at the end (but before any final empty paragraph)
                insert_index = end_index - 1
            
            # Prepare text to append
            text_to_append = ""
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
                # Join with tabs and add newline
                text_to_append += '\t'.join(row) + '\n'
            
            # Insert text at the calculated index
            requests = [{
                'insertText': {
                    'location': {'index': insert_index},
                    'text': text_to_append
                }
            }]
            
            self.service.documents().batchUpdate(
                documentId=self.document_id,
                body={'requests': requests}
            ).execute()
            
            print(f"Successfully appended {len(results)} results to Google Docs")
        except HttpError as error:
            print(f"Error appending results to Google Docs: {error}")
            raise
    
    def save_result(self, result: Dict) -> str:
        """
        Save a single ranking result to Google Docs
        
        Args:
            result: Ranking result dictionary
            
        Returns:
            Document ID (for compatibility)
        """
        self.append_results([result])
        return self.document_id
    
    def save_results(self, results: List[Dict]) -> List[str]:
        """
        Save multiple ranking results to Google Docs
        
        Args:
            results: List of ranking result dictionaries
            
        Returns:
            List containing document ID (for compatibility)
        """
        self.append_results(results)
        return [self.document_id]
    
    def get_all_results(self) -> List[List]:
        """
        Get all results from the document (reads as tab-separated text)
        
        Returns:
            List of rows from the document
        """
        try:
            doc = self.service.documents().get(documentId=self.document_id).execute()
            content = doc.get('body', {}).get('content', [])
            
            # Extract text from document
            text = ""
            for element in content:
                if 'paragraph' in element:
                    for para_element in element['paragraph'].get('elements', []):
                        if 'textRun' in para_element:
                            text += para_element['textRun'].get('content', '')
            
            # Parse tab-separated values
            rows = []
            for line in text.strip().split('\n'):
                if line.strip():
                    rows.append(line.split('\t'))
            
            return rows
        except HttpError as error:
            print(f"Error reading results from Google Docs: {error}")
            return []

