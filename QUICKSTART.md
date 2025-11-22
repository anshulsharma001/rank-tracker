# Quick Start Guide

## 🚀 Getting Started in 5 Steps

### Step 1: Get Your SerpAPI Key
1. Go to [https://serpapi.com](https://serpapi.com)
2. Sign up for a free account (100 searches/month free)
3. Copy your API key from the dashboard

### Step 2: Set Up Google Sheets
1. Create a new Google Sheet at [sheets.google.com](https://sheets.google.com)
2. Copy the Spreadsheet ID from the URL:
   - URL looks like: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
   - Copy the `SPREADSHEET_ID` part

### Step 3: Enable Google Sheets API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable **Google Sheets API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Application type: **Desktop app**
   - Download the JSON file
   - Rename it to `credentials.json` and place it in this folder

### Step 4: Configure Environment Variables
1. Open the `.env` file in this directory
2. Fill in your values:
   ```
   SERPAPI_KEY=your_actual_serpapi_key_here
   GOOGLE_SHEETS_SPREADSHEET_ID=your_actual_spreadsheet_id_here
   ```

### Step 5: Test the System
Run a test check:
```bash
python3 main.py -u https://www.example.com -k "test keyword"
```

## 📝 Example Usage

### Single Keyword
```bash
python3 main.py -u https://www.example.com -k "artificial intelligence tools"
```

### Multiple Keywords
```bash
python3 main.py -u https://www.example.com -k "AI software" "best AI companies"
```

### From CSV File
```bash
python3 main.py -u https://www.example.com -f keywords_example.csv
```

### Schedule Daily Checks
```bash
python3 scheduler.py -u https://www.example.com -k "AI tools" --daily 09:00
```

## ✅ Verify Setup
Run the setup checker:
```bash
python3 setup.py
```

This will verify that all required files and configurations are in place.

## 🆘 Need Help?
- Check the full README.md for detailed instructions
- Make sure all dependencies are installed: `pip3 install -r requirements.txt`
- Verify your API keys are correct
- Ensure credentials.json is in the project directory


