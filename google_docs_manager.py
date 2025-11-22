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
        # Default credentials file path
        default_creds_file = config.GOOGLE_SHEETS_CREDENTIALS_FILE
        
        # Check Render's secret file location first (for cloud deployments)
        render_secret_path = f"/etc/secrets/{default_creds_file}"
        if os.path.exists(render_secret_path):
            self.credentials_file = render_secret_path
        else:
            # Use provided path or default
            self.credentials_file = credentials_file or default_creds_file
        
        self.document_id = document_id or config.GOOGLE_DOCS_DOCUMENT_ID
        
        if not self.document_id:
            raise ValueError("Google Docs Document ID is required. Set GOOGLE_DOCS_DOCUMENT_ID in .env file")
        
        self.service = self._authenticate()
    
    def _authenticate(self):
        """Authenticate and return Google Docs service"""
        creds = None
        # Check Render's secret file location for token.pickle
        token_file = 'token.pickle'
        render_token_path = '/etc/secrets/token.pickle'
        if os.path.exists(render_token_path):
            token_file = render_token_path
        
        # Load existing token
        if os.path.exists(token_file):
            try:
                with open(token_file, 'rb') as token:
                    # Check if file is valid pickle by reading first few bytes
                    first_bytes = token.read(3)
                    token.seek(0)  # Reset to beginning
                    
                    # Check for common non-pickle file signatures
                    if first_bytes.startswith(b'\xef\xbb\xbf'):  # UTF-8 BOM
                        raise ValueError(
                            f"token.pickle file appears to be corrupted (UTF-8 BOM detected). "
                            f"Please regenerate token.pickle locally and re-upload to Render."
                        )
                    if first_bytes.startswith(b'{') or first_bytes.startswith(b'['):  # JSON file
                        raise ValueError(
                            f"token.pickle appears to be a JSON file, not a pickle file. "
                            f"Please regenerate token.pickle locally and re-upload to Render."
                        )
                    
                    creds = pickle.load(token)
            except (pickle.UnpicklingError, EOFError, ValueError) as e:
                # Invalid pickle file - need to regenerate
                error_msg = str(e)
                if 'invalid load key' in error_msg.lower() or '\xef' in error_msg:
                    raise ValueError(
                        f"token.pickle file is corrupted or invalid: {error_msg}\n"
                        f"This usually happens when the file is uploaded incorrectly to Render.\n\n"
                        f"To fix:\n"
                        f"1. Delete the corrupted token.pickle from Render\n"
                        f"2. Regenerate it locally: python3 -c 'from google_docs_manager import GoogleDocsManager; GoogleDocsManager()'\n"
                        f"3. Upload the new token.pickle to Render as a binary/secret file (not text)\n"
                        f"4. Make sure to upload it in binary mode (not as text content)"
                    )
                else:
                    raise
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Check if we're in a cloud environment (no browser available)
                is_cloud_env = os.getenv('RENDER') or os.getenv('HEROKU') or os.getenv('RAILWAY_ENVIRONMENT')
                
                if is_cloud_env and not os.path.exists(token_file):
                    # On cloud platforms, we can't open a browser - token.pickle must exist
                    raise FileNotFoundError(
                        f"Token file not found on cloud platform: {token_file}\n"
                        "OAuth authentication requires a browser, which is not available on cloud servers.\n\n"
                        "To fix this:\n"
                        "1. Authenticate locally on your machine:\n"
                        "   python3 -c 'from google_docs_manager import GoogleDocsManager; GoogleDocsManager()'\n"
                        "2. This will create token.pickle file locally\n"
                        "3. Upload token.pickle to Render as a 'Secret File' in Environment tab\n"
                        "4. Redeploy your service\n"
                        f"Also make sure credentials.json is uploaded as a secret file at /etc/secrets/credentials.json"
                    )
                
                # Check if credentials are provided via environment variable (for cloud deployments)
                credentials_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
                
                if credentials_json:
                    # Use credentials from environment variable
                    import json
                    import tempfile
                    creds_dict = json.loads(credentials_json)
                    # Create temporary file
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
                        json.dump(creds_dict, tmp)
                        temp_creds_file = tmp.name
                    
                    try:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            temp_creds_file, self.SCOPES)
                        
                        if is_cloud_env:
                            # On cloud, we can't use browser - must have token.pickle
                            raise FileNotFoundError(
                                "Cannot authenticate on cloud platform - browser not available.\n"
                                "Please generate token.pickle locally and upload it as a secret file."
                            )
                        
                        creds = flow.run_local_server(port=0)
                    finally:
                        # Clean up temp file
                        if os.path.exists(temp_creds_file):
                            os.unlink(temp_creds_file)
                elif os.path.exists(self.credentials_file):
                    # Use credentials from file (local development or Render secret file)
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, self.SCOPES)
                    
                    if is_cloud_env:
                        # On cloud, we can't use browser - must have token.pickle
                        raise FileNotFoundError(
                            "Cannot authenticate on cloud platform - browser not available.\n"
                            "Please generate token.pickle locally and upload it as a secret file."
                        )
                    
                    creds = flow.run_local_server(port=0)
                else:
                    # Check if credentials_file is actually JSON content (misconfiguration)
                    if self.credentials_file.strip().startswith('{'):
                        raise FileNotFoundError(
                            f"Invalid credentials configuration: The credentials path appears to be JSON content instead of a file path.\n"
                            f"On Render, make sure credentials.json is uploaded as a 'Secret File', not as an environment variable.\n"
                            f"Expected: a file path like 'credentials.json' or '/etc/secrets/credentials.json'\n"
                            f"Got: JSON content instead"
                        )
                    else:
                        raise FileNotFoundError(
                            f"Credentials file not found at: {self.credentials_file}\n"
                            "Checked locations:\n"
                            f"  - {self.credentials_file}\n"
                            f"  - /etc/secrets/{os.path.basename(self.credentials_file)}\n"
                            "On Render:\n"
                            "  1. Upload credentials.json as a 'Secret File' in the Environment tab\n"
                            "  2. Make sure the file name is exactly 'credentials.json'\n"
                            "OR set GOOGLE_CREDENTIALS_JSON environment variable with the JSON content"
                        )
            
            # Save credentials for next run (use app root, not /etc/secrets)
            save_token_file = 'token.pickle'
            if token_file.startswith('/etc/secrets/'):
                # If we loaded from /etc/secrets, save to app root
                save_token_file = 'token.pickle'
            else:
                save_token_file = token_file
            
            with open(save_token_file, 'wb') as token:
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

