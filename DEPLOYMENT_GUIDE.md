# Deployment Guide - Host Your Rank Tracker Online

## Quick Options Overview

1. **Local Network Only** - Access from your network (simple, free)
2. **Cloud Platforms** - Host online (Render, Railway, Heroku)
3. **VPS/Server** - Full control (AWS, DigitalOcean, etc.)

---

## Option 1: Access from Your Local Network (Quick & Easy)

Make your site accessible on your Wi-Fi network:

```bash
# The app already runs on 0.0.0.0, so it's accessible on your network
python3 app.py 8080
```

**To access from other devices:**
1. Find your computer's local IP:
   ```bash
   # On macOS/Linux:
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # Or:
   ipconfig getifaddr en0
   ```
2. From other devices on the same Wi-Fi, visit: `http://YOUR_IP:8080`
   - Example: `http://192.168.1.100:8080`

**Pros:** Free, easy, no setup
**Cons:** Only works on your network, not accessible from internet

---

## Option 2: Deploy to Cloud Platform (Recommended)

### A. Deploy to Render (Free tier available)

1. **Create a Render account:** https://render.com

2. **Install Render CLI** (optional):
   ```bash
   brew install render  # macOS
   ```

3. **Create these files in your project:**

   **`Procfile`:**
   ```
   web: gunicorn app:app --bind 0.0.0.0:$PORT
   ```

   **`runtime.txt`:**
   ```
   python-3.11.0
   ```

4. **Update `app.py` for production:**
   ```python
   # Change the last line from:
   app.run(debug=True, host='0.0.0.0', port=port)
   
   # To:
   if __name__ == '__main__':
       port = int(os.environ.get('PORT', 8080))
       app.run(debug=False, host='0.0.0.0', port=port)
   ```

5. **Deploy via Render Dashboard:**
   - Connect your GitHub repo
   - Select "Web Service"
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`

6. **Add environment variables in Render:**
   - `SERPAPI_KEY`
   - `GOOGLE_DOCS_DOCUMENT_ID`
   - `STORAGE_TYPE=docs`
   - `GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json`

### B. Deploy to Railway (Easy deployment)

1. **Sign up:** https://railway.app

2. **Install Railway CLI:**
   ```bash
   npm i -g @railway/cli
   ```

3. **Deploy:**
   ```bash
   railway login
   railway init
   railway up
   ```

4. **Add environment variables in Railway dashboard**

### C. Deploy to Heroku (Classic option)

1. **Install Heroku CLI:**
   ```bash
   brew tap heroku/brew && brew install heroku  # macOS
   ```

2. **Create `Procfile`:**
   ```
   web: gunicorn app:app --bind 0.0.0.0:$PORT
   ```

3. **Deploy:**
   ```bash
   heroku create your-app-name
   heroku config:set SERPAPI_KEY=your_key
   heroku config:set GOOGLE_DOCS_DOCUMENT_ID=your_id
   heroku config:set STORAGE_TYPE=docs
   git push heroku main
   ```

---

## Option 3: Production-Ready Setup

### Update `app.py` for Production

```python
# Add at the top
import os

# Change the last lines to:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)
```

### Install Production Server (Gunicorn)

Add to `requirements.txt`:
```
gunicorn==21.2.0
```

Install:
```bash
pip install gunicorn
```

Run with Gunicorn locally:
```bash
gunicorn app:app --bind 0.0.0.0:8080 --workers 2
```

---

## Important Security Considerations

### 1. Never commit credentials to git

**Create `.gitignore` (if not exists):**
```
.env
credentials.json
token.pickle
__pycache__/
*.pyc
*.pyo
```

### 2. Use environment variables

All secrets should be in environment variables, not in code:
- `SERPAPI_KEY`
- `GOOGLE_DOCS_DOCUMENT_ID`
- Google OAuth credentials

### 3. Disable debug mode in production

```python
app.run(debug=False, host='0.0.0.0', port=port)
```

---

## Step-by-Step: Render Deployment (Recommended)

### 1. Prepare your code

```bash
# Add gunicorn to requirements.txt
echo "gunicorn==21.2.0" >> requirements.txt

# Create Procfile
echo "web: gunicorn app:app --bind 0.0.0.0:\$PORT" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt
```

### 2. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 3. Deploy on Render

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Configure:
   - **Name:** rank-tracker (or your choice)
   - **Region:** Choose closest to you
   - **Branch:** main
   - **Root Directory:** (leave empty)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`

5. **Add Environment Variables:**
   - `SERPAPI_KEY` = your SerpAPI key
   - `GOOGLE_DOCS_DOCUMENT_ID` = your document ID
   - `STORAGE_TYPE` = docs
   - `GOOGLE_SHEETS_CREDENTIALS_FILE` = credentials.json
   - `PORT` = (leave empty, Render sets this)

6. **Upload credentials.json:**
   - Go to "Environment" tab
   - Use "Secret Files" section
   - Upload `credentials.json`

7. Click "Create Web Service"

### 4. Your site will be live at:
`https://your-app-name.onrender.com`

---

## Troubleshooting

### Error: "No module named gunicorn"
```bash
pip install gunicorn
echo "gunicorn==21.2.0" >> requirements.txt
```

### Error: "Credentials not found"
- Make sure you uploaded `credentials.json` as a secret file
- Or set the file path in environment variables

### Error: "Port already in use"
- Change port: `python3 app.py 3000`
- Or find and kill the process using the port

### Site not accessible
- Check firewall settings
- Make sure `host='0.0.0.0'` (not `localhost`)
- Verify port is open in cloud provider settings

---

## Quick Start for Local Network

**Simplest option - make it accessible on your Wi-Fi:**

```bash
# 1. Start the server
python3 app.py 8080

# 2. Find your IP address
ipconfig getifaddr en0  # macOS

# 3. Access from any device on your Wi-Fi:
# http://YOUR_IP:8080
```

That's it! No deployment needed for local use.

---

## Next Steps

1. **Choose your deployment method**
2. **Update app.py for production** (remove debug mode)
3. **Set up environment variables** on your platform
4. **Upload credentials.json** securely
5. **Test the deployed site**

Need help with a specific platform? Let me know!

