# Google Docs Setup Guide

## Overview

This guide will help you set up **Google Docs** to store your ranking tracking data. Your results will be automatically saved to a Google Doc that you create.

**Note:** To automatically write to Google Docs, we need API access. This requires a quick setup in Google Cloud Console (just for getting credentials - you'll still use Google Docs, not Google Cloud).

## Setup Steps

### Step 1: Create Your Google Doc (Start Here!)

1. Go to [Google Docs](https://docs.google.com/)
2. Click **"Blank"** to create a new document
3. Give it a name (e.g., "Rank Tracking Data")
4. **Get the Document ID from the URL:**
   - Look at the URL in your browser. It will look like:
     ```
     https://docs.google.com/document/d/DOCUMENT_ID_HERE/edit
     ```
   - Copy the `DOCUMENT_ID_HERE` part (the long string between `/d/` and `/edit`)
   - Save this - you'll need it later!

### Step 2: Get API Credentials (Required for Auto-Save)

To automatically save results to your Google Doc, you need API credentials. This is a one-time setup:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"New Project"** (or select existing)
3. Enter project name: "Rank Tracker" (or any name)
4. Click **"Create"**

5. Enable Google Docs API:
   - Go to **"APIs & Services"** → **"Library"**
   - Search for **"Google Docs API"**
   - Click **"Enable"**

6. Create OAuth Credentials:
   - Go to **"APIs & Services"** → **"Credentials"**
   - Click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
   - If asked, configure OAuth consent screen:
     - Choose **"External"**
     - App name: "Rank Tracker"
     - Your email for support/developer
     - Add your email as test user
     - Click through to finish
   - Back in Credentials, click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
   - Application type: **"Desktop app"**
   - Name: "Rank Tracker"
   - Click **"Create"**
   - Click **"Download JSON"**
   - Save as `credentials.json` in your project folder

7. **Share your Google Doc** with the email from your Google Cloud project:
   - Open your Google Doc
   - Click **"Share"** (top right)
   - Add the email address (the one you used for Google Cloud)
   - Give **"Editor"** access
   - Click **"Send"**

### Step 3: Configure Your Project

1. Open or create a `.env` file in your project directory
2. Add the following configuration:

```env
# SerpAPI Configuration (required)
SERPAPI_KEY=your_serpapi_key_here

# Storage Configuration
STORAGE_TYPE=docs

# Google Docs Configuration
GOOGLE_DOCS_DOCUMENT_ID=your_document_id_here

# Google OAuth Credentials (file path)
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
```

3. Replace `your_document_id_here` with the Document ID you copied in Step 5
4. Replace `your_serpapi_key_here` with your SerpAPI key (get it from [serpapi.com](https://serpapi.com))

### Step 4: Authenticate (First Run)

1. Run your first rank check:
   ```bash
   python3 main.py -u https://www.example.com -k "test keyword"
   ```

2. On first run, your browser will open automatically
3. Sign in with the Google account that has access to the document
4. Click **"Allow"** to grant permissions
5. A `token.pickle` file will be created (this stores your authentication)

### Step 5: Verify Setup

1. Run the setup checker:
   ```bash
   python3 setup.py
   ```

2. You should see:
   - ✅ .env file exists
   - ✅ SERPAPI_KEY configured
   - ✅ credentials.json exists
   - ✅ GOOGLE_DOCS_DOCUMENT_ID configured
   - ✅ Setup complete!

3. Run a test check:
   ```bash
   python3 main.py -u https://www.example.com -k "test keyword"
   ```

4. Check your Google Doc - you should see the results appended!

## How It Works

Your ranking results are automatically saved to your **Google Doc** in a table format. Each time you check rankings, new rows are added to your document.

### Data Format

Results are stored in your Google Doc with the following columns:

- **Keyword**: The keyword that was checked
- **Website URL**: The website being tracked
- **Ranking Position**: The position in search results (or "> 100" if not found)
- **Found URL**: The actual URL found in search results
- **Checked On**: Date and time of the check
- **SERP Title**: Title from the search result
- **SERP Snippet**: Description snippet from the search result
- **Notes**: Any error messages (if applicable)

## Troubleshooting

### Error: "Document ID is required"
- Make sure `GOOGLE_DOCS_DOCUMENT_ID` is set in your `.env` file
- Get the Document ID from your Google Doc URL (between `/d/` and `/edit`)

### Error: "Credentials file not found"
- Make sure `credentials.json` is in your project directory
- Download it from Google Cloud Console → Credentials → OAuth client ID

### Error: "Access denied" or "Permission denied"
- **Important:** Share your Google Doc with the email from your Google Cloud project
- Click "Share" on your Google Doc and add that email with "Editor" access
- Try deleting `token.pickle` and re-authenticating

### Error: "API not enabled"
- Go to Google Cloud Console → APIs & Services → Library
- Search for "Google Docs API" and click "Enable"

### Browser doesn't open for authentication
- Make sure you're running from a terminal
- Check terminal for a URL to copy/paste into your browser

## Using Google Docs vs Google Sheets

- **Google Docs** (`STORAGE_TYPE=docs`): Results saved to a Google Doc
- **Google Sheets** (`STORAGE_TYPE=sheets`): Results saved to a Google Sheet

Both use the same `credentials.json` file. Just change `STORAGE_TYPE` in your `.env` file.

## Important Notes

- **You're using Google Docs** - all your data goes to your Google Doc
- Google Cloud is only used to get API credentials (one-time setup)
- Keep `credentials.json` and `token.pickle` secure (don't share them)
- Add these files to `.gitignore` if using version control

## Next Steps

Once setup is complete, you can:
- Run rank checks manually: `python3 main.py -u YOUR_URL -k "keyword"`
- Use the web interface: `python3 app.py`
- Set up automated scheduling: `python3 scheduler.py`

For more information, see the main README.md file.

