# Fix: "could not locate runnable browser" Error

## The Problem
On Render (cloud platform), when trying to load history or save results, you get:
**"could not locate runnable browser"**

This happens because:
- Google OAuth requires a browser for first-time authentication
- Cloud servers (Render) don't have browsers
- The code is trying to open a browser to authenticate

## The Solution

You need to **upload `token.pickle`** to Render. This file contains your authentication token so the app doesn't need to authenticate again.

### Step 1: Generate `token.pickle` Locally

Run this on your **local machine**:

```bash
cd "/Users/anshul/Desktop/rank tracker "
python3 -c "from google_docs_manager import GoogleDocsManager; GoogleDocsManager()"
```

This will:
1. ✅ Open your browser automatically
2. ✅ Ask you to sign in with Google
3. ✅ Ask you to allow access
4. ✅ Create `token.pickle` file in your project folder

**After this runs successfully**, you'll have a `token.pickle` file locally.

### Step 2: Upload `token.pickle` to Render

1. **Go to Render Dashboard:**
   - https://dashboard.render.com
   - Click on your `rank-tracker` service

2. **Go to Environment tab:**
   - Click "Environment" tab
   - Scroll to **"Secret Files"** section

3. **Upload token.pickle:**
   - Click **"Add Secret File"** or **"Edit"** button
   - **File name:** `token.pickle`
   - **Upload the file:** Click upload and select your local `token.pickle` file
   - Save

### Step 3: Redeploy

After uploading `token.pickle`:
- Click **"Manual Deploy"** → **"Deploy latest commit"**
- Or Render will automatically redeploy (if auto-deploy is enabled)

### Step 4: Test

After redeployment:
1. Go to your live site
2. Try loading history
3. The error should be gone! ✅

---

## Why This Works

1. **First authentication** (local): Uses browser → Creates `token.pickle`
2. **Subsequent authentications**: Uses `token.pickle` → No browser needed
3. **On Render**: If `token.pickle` exists → Uses it → No browser needed ✅

---

## Quick Checklist

- [ ] Generate `token.pickle` locally (run the Python command above)
- [ ] Upload `token.pickle` to Render as Secret File
- [ ] Verify `credentials.json` is also uploaded as Secret File
- [ ] Redeploy your service
- [ ] Test loading history - should work now! ✅

---

## If You Still Get Errors

1. **Check Render logs:**
   - Go to your service → "Logs" tab
   - Look for authentication errors

2. **Verify files are uploaded:**
   - Environment → Secret Files
   - Should see both: `credentials.json` and `token.pickle`

3. **Check error message:**
   - The new code will give you clear instructions if something is wrong

---

**After uploading `token.pickle`, the browser error will be fixed!** 🎉



