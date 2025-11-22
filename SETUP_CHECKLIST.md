# Complete Setup Checklist

## ✅ What You Need to Run the System Properly

### 1. **Python Environment** ✅ (Already Installed)
- Python 3.7+ (You have 3.9.6)
- All dependencies installed via `pip3 install -r requirements.txt`

### 2. **SerpAPI Key** ✅ (Already Configured)
- ✅ Your SerpAPI key is in `.env` file
- Key: `cce06c18a41554999c42abbf8ef7992aab28efc5f2c279b210cb186ca5bccfbb`

### 3. **Google Docs Setup** ⚠️ (Needs Configuration)
**Required for storing results:**

#### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "New Project"
3. Enter project name and create

#### Step 2: Enable Google Docs API
1. Go to **APIs & Services** → **Library**
2. Search for **Google Docs API**
3. Click **Enable**

#### Step 3: Create OAuth Credentials
1. Go to **APIs & Services** → **Credentials**
2. Click **+ CREATE CREDENTIALS** → **OAuth client ID**
3. Configure OAuth consent screen (if prompted)
4. Select **Desktop app** as application type
5. Download JSON and save as `credentials.json` in project folder

#### Step 4: Create Google Doc
1. Go to [Google Docs](https://docs.google.com/)
2. Create a new blank document
3. Share it with the email from your Google Cloud project
4. Get Document ID from URL (between `/d/` and `/edit`)

#### Step 5: Verify Configuration
Your `.env` should have:
```env
STORAGE_TYPE=docs
GOOGLE_DOCS_DOCUMENT_ID=your_document_id_here
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
```

### 4. **Environment Variables** (.env file)
Check that your `.env` file contains:
```env
# SerpAPI (✅ Already set)
SERPAPI_KEY=cce06c18a41554999c42abbf8ef7992aab28efc5f2c279b210cb186ca5bccfbb

# Storage Configuration
STORAGE_TYPE=docs

# Google Docs Configuration
GOOGLE_DOCS_DOCUMENT_ID=your_document_id_here
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
```

### 5. **Required Files Checklist**
- ✅ `.env` - Environment variables
- ✅ `app.py` - Flask web server
- ✅ `templates/index.html` - Frontend HTML
- ✅ `static/css/style.css` - Frontend styles
- ✅ `static/js/app.js` - Frontend JavaScript
- ⚠️ `credentials.json` - **MISSING** (Download from Google Cloud Console)

### 6. **Dependencies** ✅ (Already Installed)
All packages from `requirements.txt`:
- ✅ requests
- ✅ google-api-python-client
- ✅ flask
- ✅ flask-cors
- ✅ python-dotenv
- ✅ schedule

---

## 🚀 Quick Setup Steps

### Step 1: Get Google Docs Credentials
```bash
# 1. Go to Google Cloud Console
# 2. Create project and enable Google Docs API
# 3. Create OAuth credentials (Desktop app)
# 4. Download as credentials.json
# 5. Create Google Doc and get Document ID
# 6. See GOOGLE_DOCS_SETUP.md for detailed steps
```

### Step 2: Verify Setup
```bash
python3 setup.py
```

This will check:
- ✅ SerpAPI key configured
- ⚠️ Google Docs credentials file exists
- ✅ All required files present

### Step 3: Start the Server
```bash
python3 app.py
```

Or use custom port:
```bash
python3 app.py 8080
```

### Step 4: Access Web Interface
Open browser: `http://localhost:8080`

---

## ⚠️ Current Issues to Fix

### Issue 1: Missing Google Docs Credentials
**Status:** ⚠️ Not configured
**Fix:** Download `credentials.json` from Google Cloud Console (see GOOGLE_DOCS_SETUP.md)

### Issue 2: Python Version Warning
**Status:** ⚠️ Warning only (not critical)
**Message:** Python 3.9.6 is past end of life
**Fix:** Optional - upgrade to Python 3.10+ (not required for now)

### Issue 3: SSL Warning
**Status:** ⚠️ Warning only (not critical)
**Message:** urllib3 SSL compatibility warning
**Fix:** Can be ignored for now, doesn't affect functionality

### Issue 4: importlib.metadata Error
**Status:** ⚠️ Error (may affect some features)
**Fix:** Try updating importlib-metadata:
```bash
pip3 install --upgrade importlib-metadata
```

---

## 🧪 Test the System

### Test 1: Check Setup
```bash
python3 setup.py
```

### Test 2: Test Rank Checking (CLI)
```bash
python3 main.py -u https://www.example.com -k "test keyword"
```

### Test 3: Start Web Server
```bash
python3 app.py 8080
```

### Test 4: Access Web Interface
1. Open browser: `http://localhost:8080`
2. Enter website URL
3. Add keywords
4. Click "Check Rankings"

---

## 📋 Complete Checklist

- [x] Python 3.7+ installed
- [x] All dependencies installed
- [x] SerpAPI key configured
- [x] `.env` file created
- [x] Storage type set to Google Docs
- [ ] **Google Cloud project created**
- [ ] **Google Docs API enabled**
- [ ] **credentials.json downloaded**
- [ ] **Google Doc created and Document ID obtained**
- [ ] Web server starts without errors
- [ ] Web interface loads in browser
- [ ] Rank checking works

---

## 🆘 If Something Doesn't Work

### Server won't start
- Check if port is in use: `lsof -ti:8080`
- Try different port: `python3 app.py 3000`
- Check for errors in terminal

### Google Docs errors
- Verify `credentials.json` exists
- Check Document ID in `.env`
- Verify Google Docs API is enabled in Google Cloud Console

### API errors
- Verify SerpAPI key is correct
- Check API quota/limits
- Test with: `python3 main.py -u https://example.com -k "test"`

### Frontend not loading
- Check server is running
- Verify correct port (8080)
- Check browser console for errors

---

## 📞 Next Steps

1. **Set up Google Docs** (Most Important!)
   - See GOOGLE_DOCS_SETUP.md for detailed instructions
   - Create Google Cloud project
   - Enable Google Docs API
   - Download credentials.json
   - Create Google Doc and get Document ID

2. **Run setup check**
   ```bash
   python3 setup.py
   ```

3. **Start the server**
   ```bash
   python3 app.py 8080
   ```

4. **Test the system**
   - Open `http://localhost:8080`
   - Try checking a ranking

---

## ✨ Once Everything is Set Up

You'll be able to:
- ✅ Check website rankings via web interface
- ✅ Upload keywords from CSV
- ✅ View ranking history
- ✅ Track multiple keywords
- ✅ Schedule automatic checks
- ✅ Export data from Google Docs

**The only missing piece is the Google Docs setup! See GOOGLE_DOCS_SETUP.md for instructions.**


