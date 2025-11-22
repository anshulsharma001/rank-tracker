# Render Deployment Checklist ✅

## Fixed Issues
- ✅ Removed `pandas` (not used, was causing build errors)
- ✅ Added `gunicorn` for production server
- ✅ Created `Procfile` for Render
- ✅ Created `runtime.txt` for Python version
- ✅ Updated `app.py` for production (uses PORT env var)

## Deployment Steps

### 1. Push Code to GitHub

```bash
# Initialize git if not done
git init
git add .
git commit -m "Ready for Render deployment"

# Push to GitHub
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 2. Deploy on Render

1. Go to: https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure settings:
   - **Name:** `rank-tracker` (or your choice)
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** (leave empty)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`

### 3. Add Environment Variables in Render

Go to **"Environment"** tab and add:

```
SERPAPI_KEY=your_serpapi_key_here
GOOGLE_DOCS_DOCUMENT_ID=1RcnA0V9QHZrBzfR0l-RR3t0mCtozbRfttDoge9RlbFA
STORAGE_TYPE=docs
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
PORT=(leave empty - Render sets this automatically)
```

### 4. Upload credentials.json as Secret File

1. In Render dashboard, go to **"Environment"** tab
2. Scroll to **"Secret Files"** section
3. Click **"Add Secret File"**
4. **File name:** `credentials.json`
5. **File contents:** Paste the entire contents of your `credentials.json` file

### 5. Deploy!

Click **"Create Web Service"** and wait for deployment.

## Important Notes

⚠️ **Free Tier Limitations:**
- Free instances spin down after 15 minutes of inactivity
- First request after spin-down can take 50+ seconds
- Consider upgrading for production use

✅ **After Deployment:**
- Your site will be at: `https://your-app-name.onrender.com`
- Check logs if there are any issues
- Test the `/api/check-rankings` endpoint

## Troubleshooting

### Build Fails
- Check logs for specific error
- Make sure all dependencies are in `requirements.txt`
- Verify Python version in `runtime.txt` is compatible

### App Crashes
- Check environment variables are set correctly
- Verify `credentials.json` is uploaded as secret file
- Check logs for authentication errors

### Can't Access Google Docs
- Make sure Google Doc is shared with your Google account
- Verify `GOOGLE_DOCS_DOCUMENT_ID` is correct
- Check OAuth token is valid (may need to re-authenticate)

---

**Your deployment should work now!** The build error is fixed by removing pandas.

