# Fix: "invalid load key, '\xef.'" Error

## The Problem
You're seeing the error: **"invalid load key, '\xef.'"**

This happens when `token.pickle` file is **corrupted** or **uploaded incorrectly** to Render.

## Why This Happens

When uploading `token.pickle` to Render's Secret Files, if you:
- Copy/paste the file content as text
- Upload it in text mode instead of binary mode
- The file gets corrupted during upload

The file gets corrupted and can't be read by Python's pickle module.

## The Solution

### Option 1: Upload File Correctly (Recommended)

1. **Delete the corrupted token.pickle from Render:**
   - Go to Render Dashboard → Your Service → Environment tab
   - Scroll to Secret Files section
   - Find `token.pickle` and delete it

2. **On your local machine, verify token.pickle is valid:**
   ```bash
   cd "/Users/anshul/Desktop/rank tracker "
   python3 -c "import pickle; f=open('token.pickle','rb'); pickle.load(f); print('✅ Valid!')"
   ```
   Should print: `✅ Valid!`

3. **Upload token.pickle correctly to Render:**
   - Go to Render → Environment → Secret Files
   - Click "Add Secret File" or "Edit"
   - **File name:** `token.pickle`
   - **IMPORTANT:** Click "Upload File" button and select your local `token.pickle` file
   - **DO NOT** copy/paste file content as text
   - **DO NOT** use text mode - use binary file upload
   - Click "Save"

4. **Redeploy:**
   - After uploading, click "Manual Deploy" → "Deploy latest commit"

### Option 2: Regenerate token.pickle

If the local file is also corrupted:

1. **Delete old token.pickle locally:**
   ```bash
   rm token.pickle
   ```

2. **Regenerate it:**
   ```bash
   python3 -c "from google_docs_manager import GoogleDocsManager; GoogleDocsManager()"
   ```
   This will open your browser for authentication.

3. **Upload the new token.pickle to Render** (see Option 1, step 3)

## Important Notes

✅ **DO:**
- Upload `token.pickle` as a **binary file** using the file upload button
- Make sure to use "Upload File" not "Paste text"

❌ **DON'T:**
- Copy/paste the file content as text
- Open the file and paste its contents
- Upload in text mode

## How to Verify Upload Worked

After uploading and redeploying:
1. Go to your live site
2. Click "Load History"
3. If you see data (or "No history found" if empty), the file is working ✅
4. If you still see the error, the file is still corrupted - try Option 2

---

## Summary Checklist

- [ ] Delete corrupted `token.pickle` from Render (if exists)
- [ ] Verify local `token.pickle` is valid (run the Python command above)
- [ ] Upload `token.pickle` to Render using "Upload File" button (binary upload)
- [ ] Redeploy your service
- [ ] Test loading history - should work now! ✅

---

**The key is to upload the file as a binary file, not as text content!** 🎯



