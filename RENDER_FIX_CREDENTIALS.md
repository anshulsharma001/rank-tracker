# Fix: Credentials File Error on Render

## The Problem
Your Render deployment shows: "Credentials file not found" error.

## The Solution

### Option 1: Upload credentials.json as Secret File (Recommended)

1. **Go to Render Dashboard:**
   - Open your service: https://dashboard.render.com
   - Click on your `rank-tracker` service
   - Go to **"Environment"** tab

2. **Upload credentials.json:**
   - Scroll to **"Secret Files"** section
   - Click **"Add Secret File"** or **"Upload File"**
   - **File name:** `credentials.json`
   - **File contents:** Copy the entire contents from your local `credentials.json` file
   - **Note:** Get this file from your local machine (it should NOT be in git)

3. **Generate token.pickle locally and upload it:**

   The first time, OAuth needs browser authentication. Do this locally:

   ```bash
   # On your local machine
   cd "/Users/anshul/Desktop/rank tracker "
   python3 -c "
   from google_docs_manager import GoogleDocsManager
   manager = GoogleDocsManager()
   print('✅ Token created!')
   "
   ```

   This will:
   - Open your browser
   - Ask you to sign in
   - Create `token.pickle` file

4. **Upload token.pickle to Render:**
   - In Render → Environment → Secret Files
   - Click **"Add Secret File"**
   - **File name:** `token.pickle`
   - **Upload the file** from your local machine

5. **Redeploy:**
   - After uploading both files, click **"Manual Deploy"** → **"Deploy latest commit"**

---

### Option 2: Use Environment Variable (Alternative)

1. **In Render Dashboard → Environment:**
   - Add new environment variable:
   - **Name:** `GOOGLE_CREDENTIALS_JSON`
   - **Value:** The entire JSON content from your `credentials.json` file (minified to one line)
   - **Note:** Get this from your local `credentials.json` file - never commit secrets to git!

2. **Still need to generate token.pickle locally:**
   - Follow step 3 from Option 1
   - Upload token.pickle as secret file

---

## Why token.pickle is Needed

OAuth requires browser interaction the first time. Once you authenticate locally:
- A `token.pickle` file is created
- This file contains your authentication token
- Upload this file to Render so it doesn't need to authenticate again
- The token will refresh automatically when needed

---

## Quick Steps Summary

1. ✅ Upload `credentials.json` as secret file in Render
2. ✅ Generate `token.pickle` locally (run the Python code above)
3. ✅ Upload `token.pickle` as secret file in Render  
4. ✅ Redeploy your service

After this, your site should work! 🎉

---

## If It Still Doesn't Work

Check the Render logs:
- Go to your service → "Logs" tab
- Look for any authentication errors
- Make sure both files are uploaded correctly

The error should be gone after uploading both files!

