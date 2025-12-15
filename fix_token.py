#!/usr/bin/env python3
"""
Script to regenerate token.pickle for deployment
This ensures the token is created correctly for uploading to Render
"""
import os
import sys

def main():
    print("=" * 60)
    print("Token Regeneration Script")
    print("=" * 60)
    print()
    
    # Check if token.pickle exists
    if os.path.exists('token.pickle'):
        response = input("token.pickle already exists. Delete and regenerate? (y/n): ")
        if response.lower() == 'y':
            os.remove('token.pickle')
            print("✅ Deleted old token.pickle")
        else:
            print("Keeping existing token.pickle")
            return
    
    print("\n🔐 Starting authentication...")
    print("A browser window will open for you to sign in with Google.")
    print("After signing in, token.pickle will be created.\n")
    
    try:
        from google_docs_manager import GoogleDocsManager
        manager = GoogleDocsManager()
        print("\n✅ Authentication successful!")
        print("✅ token.pickle created successfully")
        print()
        print("=" * 60)
        print("Next Steps for Render Deployment:")
        print("=" * 60)
        print("1. Go to Render Dashboard → Your Service → Environment")
        print("2. Go to 'Secret Files' section")
        print("3. Delete the old 'token' secret file if it exists")
        print("4. Click 'Add Secret File'")
        print("5. Name: token")
        print("6. Upload the token.pickle file from this directory")
        print("7. Destination: /etc/secrets/token.pickle")
        print("8. IMPORTANT: Make sure to upload as BINARY, not text!")
        print("9. Save and redeploy your service")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure credentials.json exists")
        print("2. Make sure GOOGLE_DOCS_DOCUMENT_ID is set in .env")
        print("3. Check that Google Docs API is enabled in Google Cloud Console")
        sys.exit(1)

if __name__ == '__main__':
    main()

