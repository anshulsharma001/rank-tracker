# Automated Google Rank Tracking System

An automated system to check and track the ranking position of a website on Google Search for specified keywords. Results are automatically stored in Google Sheets for easy tracking and analysis.

## Features

- ✅ Check ranking positions for single or multiple keywords
- ✅ Support for bulk keyword lists via CSV files
- ✅ Automatic data storage in Google Sheets
- ✅ Scheduled automated checks (daily, weekly, or custom intervals)
- ✅ Tracks up to top 100 search results
- ✅ Extracts SERP title and snippet information
- ✅ Uses authorized SerpAPI (compliant with Google's Terms of Service)

## Prerequisites

1. **Python 3.7+** installed on your system
2. **SerpAPI Account** - Sign up at [https://serpapi.com](https://serpapi.com) to get your API key
3. **Google Cloud Project** with Sheets API enabled
4. **Google OAuth 2.0 Credentials** - Download credentials.json from Google Cloud Console

## Installation

### 1. Clone or download this repository

```bash
cd "/Users/anshul/Desktop/rank tracker "
```

### 2. Install required packages

```bash
pip install -r requirements.txt
```

### 3. Set up SerpAPI

1. Sign up for a free account at [https://serpapi.com](https://serpapi.com)
2. Get your API key from the dashboard
3. Add it to your `.env` file (see Configuration section)

### 4. Set up Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Sheets API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as application type
   - Download the JSON file and save it as `credentials.json` in the project directory

### 5. Create a Google Sheet

1. Create a new Google Sheet
2. Copy the Spreadsheet ID from the URL:
   - URL format: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
   - The `SPREADSHEET_ID` is the long string between `/d/` and `/edit`

### 6. Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   SERPAPI_KEY=your_serpapi_key_here
   GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
   ```

3. Place your `credentials.json` file in the project directory

## Usage

### Basic Usage - Single Keyword

```bash
python main.py -u https://www.example.com -k "artificial intelligence tools"
```

### Multiple Keywords

```bash
python main.py -u https://www.example.com -k "AI software" "best AI companies" "machine learning platforms"
```

### Using CSV File

1. Create a CSV file with keywords (one per line):
   ```csv
   artificial intelligence tools
   AI software
   best AI companies
   ```

2. Run the script:
   ```bash
   python main.py -u https://www.example.com -f keywords.csv
   ```

### Custom Location

```bash
python main.py -u https://www.example.com -k "AI tools" --location "United Kingdom"
```

### Custom Sheet Name

```bash
python main.py -u https://www.example.com -k "AI tools" --sheet-name "My Rankings"
```

## Automated Scheduling

### Daily Check

Run a check every day at 9:00 AM:
```bash
python scheduler.py -u https://www.example.com -k "AI tools" --daily 09:00
```

### Weekly Check

Run every Monday at 10:00 AM:
```bash
python scheduler.py -u https://www.example.com -k "AI tools" --weekly monday 10:00
```

### Every N Hours

Run every 6 hours:
```bash
python scheduler.py -u https://www.example.com -k "AI tools" --hours 6
```

### Every N Minutes

Run every 30 minutes:
```bash
python scheduler.py -u https://www.example.com -k "AI tools" --minutes 30
```

**Note:** The scheduler will run continuously. Press `Ctrl+C` to stop it.

## Google Sheets Output

The system automatically creates a sheet (if it doesn't exist) with the following columns:

| Column | Description |
|--------|-------------|
| Keyword | The search keyword |
| Website URL | The URL being tracked |
| Ranking Position | Position number (or "> 100" if not found) |
| Found URL | The actual URL found in search results |
| Checked On | Date and time of the check |
| SERP Title | Title from search results |
| SERP Snippet | Snippet from search results |
| Notes | Error messages (if any) |

## Project Structure

```
rank tracker/
├── main.py                 # Main application script
├── rank_checker.py         # Google search ranking checker
├── google_sheets_manager.py # Google Sheets integration
├── scheduler.py            # Automated scheduling
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── keywords_example.csv   # Example keywords file
├── README.md              # This file
└── credentials.json       # Google OAuth credentials (not in repo)
```

## Configuration Options

Edit `config.py` to customize:

- `MAX_RESULTS_TO_CHECK`: Maximum results to check (default: 100)
- `RESULTS_PER_PAGE`: Results per page (default: 10)
- `USE_GOOGLE_SHEETS`: Enable/disable Google Sheets storage (default: True)

## Error Handling

The system handles various error scenarios:

- **API Errors**: Displays error message and continues with other keywords
- **Network Issues**: Retries with appropriate error messages
- **Missing Credentials**: Clear error messages guiding setup
- **Sheet Access Issues**: Falls back gracefully

## Rate Limiting

The system includes built-in rate limiting to respect API limits:

- 1 second delay between pages
- 2 seconds delay between keywords
- Adjustable in the code if needed

## Troubleshooting

### "SerpAPI key is required" Error
- Make sure you've created a `.env` file with `SERPAPI_KEY=your_key`

### "Credentials file not found" Error
- Download `credentials.json` from Google Cloud Console
- Place it in the project directory

### "Spreadsheet ID is required" Error
- Add `GOOGLE_SHEETS_SPREADSHEET_ID` to your `.env` file
- Get the ID from your Google Sheet URL

### Authentication Issues
- Delete `token.pickle` and re-authenticate
- Make sure OAuth consent screen is configured in Google Cloud Console

### No Results Found
- Check if the website is actually ranking for the keyword
- Verify the URL format (with or without https://)
- Try different keyword variations

## API Costs

**SerpAPI Pricing:**
- Free tier: 100 searches/month
- Paid plans available for higher volumes

**Google Sheets API:**
- Free for personal use
- No additional costs for API calls

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all API keys and credentials are correct
3. Ensure all dependencies are installed

## Future Enhancements

Potential improvements:
- Support for multiple search engines
- Email notifications for ranking changes
- Historical ranking trend analysis
- Dashboard visualization
- Export to other formats (CSV, JSON)

---

**Note:** This system uses authorized APIs and complies with Google's Terms of Service. Direct scraping of Google results is not used.


