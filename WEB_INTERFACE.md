# Web Interface Guide

## 🚀 Quick Start

The web interface combines both frontend and backend in one Flask application.

### Starting the Server

**Option 1: Using the start script**
```bash
./start_server.sh
```

**Option 2: Direct Python command**
```bash
python3 app.py
```

The server will start on **http://localhost:8080** (ports 5000/5001 are often used by AirPlay on macOS)

### Accessing the Web Interface

1. Open your web browser
2. Go to: **http://localhost:8080**
3. You'll see the Google Rank Tracker interface

---

## 📋 Features

### 1. Check Rankings
- Enter your website URL
- Add keywords (one per line)
- Select location (optional)
- Click "Check Rankings"
- View results instantly

### 2. Upload CSV
- Click "Upload CSV" button
- Select a CSV file with keywords
- Keywords will be automatically loaded

### 3. View History
- Filter by website URL (optional)
- Filter by keyword (optional)
- Click "Load History"
- View past ranking checks

---

## 🎨 Interface Overview

### Main Form
- **Website URL**: The website you want to track
- **Keywords**: One keyword per line
- **Location**: Search location (default: United States)
- **Check Rankings**: Submit the form
- **Upload CSV**: Load keywords from file

### Results Display
- ✅ **Green**: Website found in results
- ⚠️ **Yellow**: Website not in top 100
- ❌ **Red**: Error occurred

### History Section
- View all past checks
- Filter by website or keyword
- See ranking changes over time

---

## 🔧 API Endpoints

The backend provides these API endpoints:

### POST `/api/check-rankings`
Check website rankings for keywords.

**Request:**
```json
{
  "website_url": "https://www.example.com",
  "keywords": ["keyword1", "keyword2"],
  "location": "United States"
}
```

**Response:**
```json
{
  "success": true,
  "results": [...],
  "saved": true,
  "website_url": "...",
  "location": "..."
}
```

### GET `/api/history`
Get ranking history.

**Query Parameters:**
- `website_url` (optional): Filter by website
- `keyword` (optional): Filter by keyword
- `limit` (optional): Number of results (default: 50)

### POST `/api/upload-keywords`
Upload keywords from CSV file.

**Request:** Multipart form data with `file` field

**Response:**
```json
{
  "success": true,
  "keywords": ["keyword1", "keyword2"],
  "count": 2
}
```

---

## 🛠️ Troubleshooting

### Server won't start
- Check if port 5000 is already in use
- Make sure all dependencies are installed: `pip3 install -r requirements.txt`
- Verify your `.env` file is configured

### API errors
- Check SerpAPI key in `.env` file
- Verify Google Docs/Sheets credentials if using Google Docs/Sheets
- Check network connection

### Frontend not loading
- Make sure you're accessing `http://localhost:8080`
- Check browser console for errors
- Verify Flask is running
- If port 8080 is also in use, run: `python3 app.py 3000` to use a different port

---

## 📱 Mobile Friendly

The interface is responsive and works on:
- Desktop browsers
- Tablets
- Mobile phones

---

## 🔒 Security Notes

- The server runs on `0.0.0.0:5000` by default (accessible from network)
- For production, use a proper web server (nginx + gunicorn)
- Add authentication if exposing to internet
- Keep API keys secure in `.env` file

---

## 🎯 Next Steps

1. **Start the server**: `python3 app.py`
2. **Open browser**: Go to `http://localhost:8080`
3. **Enter your website URL and keywords**
4. **Click "Check Rankings"**
5. **View results and history**

**Note**: If you want to use a different port, run: `python3 app.py 3000` (replace 3000 with your preferred port)

Enjoy tracking your website rankings! 🚀

