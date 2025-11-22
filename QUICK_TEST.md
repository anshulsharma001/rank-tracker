# 🚀 Quick Test - Get Started in 30 Seconds

## Option 1: Web Interface (Easiest)

1. **Start server:**
   ```bash
   python3 app.py 8080
   ```

2. **Open browser:**
   ```
   http://localhost:8080
   ```

3. **Enter this test data:**
   - **Website URL:** `https://www.google.com`
   - **Keywords:**
     ```
     google
     ```

4. **Click "Check Rankings"**

5. **Expected Result:**
   - ✅ Should show "Position 1" (Google ranks #1 for "google")

---

## Option 2: Command Line (Fastest)

```bash
python3 main.py -u https://www.google.com -k "google"
```

**Expected Output:**
```
✅ google: Position 1 - https://www.google.com
```

---

## ✅ Success Indicators

- ✅ Server starts without errors
- ✅ Results show position numbers
- ✅ No error messages
- ✅ Results are saved (check Google Docs/Sheets)

---

## 🎯 Next Tests to Try

### Test 2: Multiple Keywords
```bash
python3 main.py -u https://www.google.com -k "google" "search engine" "web browser"
```

### Test 3: Different Website
```bash
python3 main.py -u https://www.wikipedia.org -k "wikipedia"
```

### Test 4: Your Website
```bash
python3 main.py -u https://yourwebsite.com -k "your keyword"
```

---

## 🆘 If Test Fails

1. **Check SerpAPI key:**
   ```bash
   python3 setup.py
   ```

2. **Check Google Docs/Sheets (if using):**
   - Verify `credentials.json` exists
   - Check Document ID or Spreadsheet ID in `.env`

3. **Check server:**
   - Make sure it's running on port 8080
   - Try: `curl http://localhost:8080`

---

**That's it! If you see Position 1 for Google, everything is working! 🎉**


