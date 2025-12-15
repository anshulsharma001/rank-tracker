# Deployment Guide - Make Your Rank Tracker Live

This guide will help you deploy your Rank Tracker to **Render** (free tier available) so it's accessible online.

## Quick Deploy to Render

### Step 1: Prepare Your Files

1. **Push to GitHub** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

### Step 2: Deploy on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `rank-tracker` (or any name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python3 app.py 8080`

### Step 3: Set Environment Variables

In Render dashboard, go to **Environment** tab and add:

```
SERPAPI_KEY=your_serpapi_key_here
STORAGE_TYPE=docs
GOOGLE_DOCS_DOCUMENT_ID=your_document_id_here
GOOGLE_SHEETS_CREDENTIALS_FILE=/etc/secrets/credentials.json
```

### Step 4: Upload Secret Files

1. **Upload credentials.json**:
   - Go to **Environment** → **Secret Files**
   - Click **"Add Secret File"**
   - Name: `credentials`
   - Upload your `credentials.json` file
   - Destination: `/etc/secrets/credentials.json`

2. **Upload token.pickle** (IMPORTANT - Must be binary!):
   - First, create it locally using the helper script:
     ```bash
     python3 fix_token.py
     ```
     Or manually:
     ```bash
     python3 -c "from google_docs_manager import GoogleDocsManager; GoogleDocsManager()"
     ```
   - This will open a browser for authentication
   - After authentication, `token.pickle` will be created
   - **CRITICAL**: Upload it as a secret file:
     - Name: `token`
     - Upload `token.pickle` file
     - Destination: `/etc/secrets/token.pickle`
     - **⚠️ Make sure to upload as BINARY file, NOT as text!**
     - In Render, when uploading, ensure it's uploaded as a file attachment, not pasted text

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (usually 2-3 minutes)
3. Your app will be live at: `https://your-app-name.onrender.com`

## Alternative: Deploy with render.yaml

If you have `render.yaml` in your repo:

1. Go to Render Dashboard
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repo
4. Render will automatically detect `render.yaml` and configure everything

## Important Notes

### Authentication on Render

- The app needs `token.pickle` to authenticate with Google Docs
- You must create this file **locally first**, then upload it to Render
- If token expires, you'll need to re-upload it

### Fixing "token.pickle corrupted" Error

If you see this error: `token.pickle file is corrupted or invalid: invalid load key, '\xef'`

**This means the file was uploaded as text instead of binary!**

**Quick Fix:**

1. **Regenerate token locally:**
   ```bash
   python3 fix_token.py
   ```
   Or:
   ```bash
   rm token.pickle
   python3 -c "from google_docs_manager import GoogleDocsManager; GoogleDocsManager()"
   ```

2. **Delete old token on Render:**
   - Go to Render Dashboard → Your Service → Environment
   - Find the "token" secret file
   - Delete it

3. **Upload new token correctly:**
   - Click "Add Secret File"
   - Name: `token`
   - **Upload the file** (don't copy/paste text!)
   - Destination: `/etc/secrets/token.pickle`
   - **Make sure you're uploading the actual file, not pasting its contents**

4. **Redeploy** your service

### Updating token.pickle

If you get authentication errors:

1. Delete old `token.pickle` locally
2. Re-authenticate:
   ```bash
   python3 fix_token.py
   ```
3. Upload new `token.pickle` to Render as a secret file (as binary, not text!)

### Free Tier Limitations

- Render free tier: App sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- Consider upgrading for always-on service

## Troubleshooting

### App won't start
- Check build logs in Render dashboard
- Verify all environment variables are set
- Make sure `credentials.json` and `token.pickle` are uploaded

### Authentication errors
- Verify `token.pickle` is uploaded correctly
- Check that Google Doc is shared with the correct email
- Re-upload `token.pickle` if expired

### Port issues
- Render automatically sets `PORT` environment variable
- The app uses port 8080 by default, but Render may use a different port
- Check Render logs for the actual port being used

## Other Deployment Options

### Railway
1. Go to [Railway](https://railway.app/)
2. Connect GitHub repo
3. Add environment variables
4. Upload secrets via Railway dashboard

### Heroku
1. Install Heroku CLI
2. `heroku create your-app-name`
3. `git push heroku main`
4. Set environment variables via `heroku config:set`

### DigitalOcean App Platform
1. Create new app
2. Connect GitHub
3. Configure build/start commands
4. Add environment variables and secrets

## Post-Deployment

After deployment:
1. Test your live URL
2. Check that rankings are being saved to Google Docs
3. Monitor logs for any errors
4. Share your live URL with others!

---

**Need help?** Check the logs in your deployment platform's dashboard for detailed error messages.

