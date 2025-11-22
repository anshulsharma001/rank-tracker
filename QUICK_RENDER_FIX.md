# Quick Fix for Render Credentials Error

## The Problem
The error shows: `Credentials file not found: { "installed": { ...` 

This means Render is trying to use the JSON content as a file path, not an actual file.

## The Solution

### 1. Check Environment Variables in Render

Go to Render Dashboard → Your Service → Environment tab

**Make sure `GOOGLE_SHEETS_CREDENTIALS_FILE` is set to JUST the filename:**
- ✅ **Correct:** `credentials.json` (just the filename)
- ❌ **Wrong:** `{ "installed": { ... } }` (JSON content)

**If it's wrong, fix it:**
1. Click "Edit" next to `GOOGLE_SHEETS_CREDENTIALS_FILE`
2. Change the value to: `credentials.json`
3. Save

### 2. Verify Secret File is Uploaded

In the same Environment tab → Scroll to "Secret Files" section:

**Should show:**
- **FILENAME:** `credentials.json`
- **CONTENTS:** (eye icon - hidden)

**If it's not there:**
1. Click "Add Secret File" or "Edit"
2. **File name:** `credentials.json`
3. **Contents:** Paste your entire credentials.json content from your local `credentials.json` file

**Note:** Get your credentials.json from your local machine - do NOT commit this file to git!

4. Save

### 3. Generate token.pickle Locally

Run this on your computer:

```bash
cd "/Users/anshul/Desktop/rank tracker "
python3 -c "from google_docs_manager import GoogleDocsManager; GoogleDocsManager()"
```

This will:
- Open your browser
- Ask you to sign in to Google
- Create `token.pickle` file

### 4. Upload token.pickle to Render

In Render → Environment → Secret Files:
1. Click "Add Secret File"
2. **File name:** `token.pickle`
3. Upload the `token.pickle` file from your computer

### 5. Redeploy

Click "Manual Deploy" → "Deploy latest commit"

---

## Summary Checklist

- [ ] `GOOGLE_SHEETS_CREDENTIALS_FILE` = `credentials.json` (NOT JSON content)
- [ ] `credentials.json` uploaded as Secret File
- [ ] `token.pickle` generated locally
- [ ] `token.pickle` uploaded as Secret File
- [ ] Redeployed service

After these steps, the error should be gone! ✅

