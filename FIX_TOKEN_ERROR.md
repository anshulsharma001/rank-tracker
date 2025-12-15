# Fix "token.pickle corrupted" Error

## The Problem

You're seeing this error when loading history:
```
token.pickle file is corrupted or invalid: invalid load key, '\xef'
```

This happens when `token.pickle` was uploaded to Render as **text** instead of **binary**.

## Quick Fix (5 minutes)

### Step 1: Regenerate token.pickle locally

Run this command:
```bash
python3 fix_token.py
```

Or manually:
```bash
rm token.pickle  # Delete old one
python3 -c "from google_docs_manager import GoogleDocsManager; GoogleDocsManager()"
```

A browser will open - sign in with Google and allow access.

### Step 2: Delete corrupted token on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click on your service (rank-tracker)
3. Go to **Environment** tab
4. Scroll to **Secret Files** section
5. Find the `token` secret file
6. Click **Delete** or **Remove**

### Step 3: Upload new token correctly

1. Still in **Environment** → **Secret Files**
2. Click **"Add Secret File"**
3. Fill in:
   - **Name**: `token`
   - **File**: Click "Choose File" and select `token.pickle` from your project folder
   - **Destination**: `/etc/secrets/token.pickle`
4. **IMPORTANT**: Make sure you're uploading the file itself, not copying/pasting text!
5. Click **Save**

### Step 4: Redeploy

1. Go to **Manual Deploy** tab (or it may auto-deploy)
2. Click **"Deploy latest commit"** or **"Clear build cache & deploy"**
3. Wait 2-3 minutes for deployment

### Step 5: Test

1. Go to your live URL: `https://rank-tracker-5xay.onrender.com`
2. Try loading history again
3. It should work now! ✅

## Why This Happens

- `token.pickle` is a binary file (Python pickle format)
- If you copy/paste its contents or upload it as text, it gets corrupted
- Render needs the actual binary file, uploaded as a file attachment

## Prevention

Always use the file upload feature in Render, never copy/paste the contents of `token.pickle`.

## Still Having Issues?

1. **Check file size**: `token.pickle` should be around 1-2 KB
2. **Verify locally**: Make sure `token.pickle` works locally first
3. **Check logs**: Look at Render logs for more details
4. **Re-authenticate**: Sometimes tokens expire - regenerate and re-upload

## Need More Help?

Check the full deployment guide: `DEPLOYMENT.md`

