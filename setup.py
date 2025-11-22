#!/usr/bin/env python3
"""
Setup script to help configure the Google Rank Tracking System
"""
import os
import sys

def check_setup():
    """Check if the system is properly configured"""
    print("=" * 60)
    print("Google Rank Tracking System - Setup Check")
    print("=" * 60)
    print()
    
    issues = []
    
    # Check .env file
    if not os.path.exists('.env'):
        issues.append("❌ .env file not found")
        print("❌ .env file not found")
        print("   → Copy .env.example to .env and add your API keys")
    else:
        print("✅ .env file exists")
        # Check if it has values
        from dotenv import load_dotenv
        load_dotenv()
        if not os.getenv('SERPAPI_KEY') or os.getenv('SERPAPI_KEY') == 'your_serpapi_key_here':
            issues.append("❌ SERPAPI_KEY not configured in .env")
            print("❌ SERPAPI_KEY not configured")
        else:
            print("✅ SERPAPI_KEY configured")
        
    
    # Check storage type
    storage_type = os.getenv('STORAGE_TYPE', 'docs').lower()
    print(f"Storage type: {storage_type}")
    
    # Check Google credentials (needed for both Docs and Sheets)
    if not os.path.exists('credentials.json'):
        issues.append("❌ credentials.json not found")
        print("❌ credentials.json not found")
        print("   → Download OAuth 2.0 credentials from Google Cloud Console")
    else:
        print("✅ credentials.json exists")
    
    # Check document/spreadsheet ID
    if storage_type == 'docs':
        docs_id = os.getenv('GOOGLE_DOCS_DOCUMENT_ID')
        if not docs_id or docs_id == 'your_document_id_here':
            issues.append("❌ GOOGLE_DOCS_DOCUMENT_ID not configured in .env")
            print("❌ GOOGLE_DOCS_DOCUMENT_ID not configured")
        else:
            print("✅ GOOGLE_DOCS_DOCUMENT_ID configured")
    elif storage_type == 'sheets':
        sheets_id = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
        if not sheets_id or sheets_id == 'your_spreadsheet_id_here':
            issues.append("❌ GOOGLE_SHEETS_SPREADSHEET_ID not configured in .env")
            print("❌ GOOGLE_SHEETS_SPREADSHEET_ID not configured")
        else:
            print("✅ GOOGLE_SHEETS_SPREADSHEET_ID configured")
    
    print()
    print("=" * 60)
    
    if issues:
        print("\n⚠️  Setup incomplete. Please fix the issues above.")
        print("\nQuick Setup Guide:")
        print("1. Get SerpAPI key from: https://serpapi.com")
        if storage_type == 'docs':
            print("2. Create Google Doc and get Document ID from URL")
            print("3. Enable Google Docs API in Google Cloud Console")
            print("4. Download OAuth credentials as credentials.json")
            print("5. Update .env with your configuration")
        else:
            print("2. Create Google Sheet and get Spreadsheet ID from URL")
            print("3. Enable Google Sheets API in Google Cloud Console")
            print("4. Download OAuth credentials as credentials.json")
            print("5. Update .env with your configuration")
        return False
    else:
        print("\n✅ Setup complete! You're ready to use the system.")
        return True

if __name__ == '__main__':
    try:
        check_setup()
    except ImportError:
        print("Error: python-dotenv not installed. Run: pip3 install -r requirements.txt")
        sys.exit(1)

