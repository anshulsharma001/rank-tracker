# Testing Guide - How to Test the Rank Tracker

## 🧪 Quick Test Methods

### Method 1: Test via Web Interface (Recommended)

1. **Start the server:**
   ```bash
   python3 app.py 8080
   ```

2. **Open browser:**
   Go to: `http://localhost:8080`

3. **Enter test data:**
   - **Website URL:** `https://www.google.com`
   - **Keywords:** (one per line)
     ```
     search engine
     web browser
     google search
     ```

4. **Click "Check Rankings"**

5. **View results:**
   - You should see Google's ranking positions
   - Results will be color-coded (green = found, yellow = not in top 100)

---

### Method 2: Test via Command Line

```bash
python3 main.py -u https://www.google.com -k "search engine" "web browser"
```

**Expected output:**
```
============================================================
Google Rank Tracking System
============================================================
Website URL: https://www.google.com
Keywords to check: 2
Location: United States
============================================================

Starting rank checks...

============================================================
Ranking Results:
============================================================
✅ search engine: Position 1 - https://www.google.com
✅ web browser: Position 1 - https://www.google.com

============================================================
Rank tracking completed!
============================================================
```

---

## 📝 Test Examples

### Example 1: Test with Google (Should Rank #1)
```bash
python3 main.py -u https://www.google.com -k "google"
```
**Expected:** Position 1 (Google ranks #1 for "google")

### Example 2: Test with Wikipedia
```bash
python3 main.py -u https://www.wikipedia.org -k "wikipedia" "encyclopedia"
```
**Expected:** Should find Wikipedia in top results

### Example 3: Test with Your Own Website
```bash
python3 main.py -u https://yourwebsite.com -k "your brand name" "your main keyword"
```
**Expected:** Shows where your website ranks

### Example 4: Test Multiple Keywords
```bash
python3 main.py -u https://www.example.com -k "keyword1" "keyword2" "keyword3"
```

### Example 5: Test from CSV File
```bash
python3 main.py -u https://www.example.com -f keywords_example.csv
```

---

## 🌐 Good Test Websites

### High-Ranking Sites (Easy to Test)
- **Google:** `https://www.google.com` - Keywords: "google", "search engine"
- **Wikipedia:** `https://www.wikipedia.org` - Keywords: "wikipedia", "encyclopedia"
- **YouTube:** `https://www.youtube.com` - Keywords: "youtube", "video"
- **Amazon:** `https://www.amazon.com` - Keywords: "amazon", "online shopping"

### Why These Work Well:
- They rank highly for their brand names
- Easy to verify results
- Good for testing the system

---

## ✅ Step-by-Step Testing Process

### Test 1: Basic Functionality
1. Start server: `python3 app.py 8080`
2. Open `http://localhost:8080`
3. Enter:
   - URL: `https://www.google.com`
   - Keyword: `google`
4. Click "Check Rankings"
5. **Expected:** Should show Position 1

### Test 2: Multiple Keywords
1. Same as above, but add multiple keywords:
   ```
   google
   search engine
   web browser
   ```
2. **Expected:** Should show results for all keywords

### Test 3: CSV Upload
1. Use the example CSV: `keywords_example.csv`
2. Click "Upload CSV" button
3. Select the file
4. **Expected:** Keywords should load into the form

### Test 4: History View
1. After running some checks
2. Scroll to "View History" section
3. Click "Load History"
4. **Expected:** Should show past ranking checks

---

## 🔍 What to Look For

### ✅ Success Indicators:
- ✅ Server starts without errors
- ✅ Web interface loads
- ✅ Form accepts input
- ✅ Results display correctly
- ✅ Results saved to Google Docs/Sheets
- ✅ History shows past checks

### ⚠️ Warning Signs:
- ⚠️ "> 100" - Website not in top 100 (normal for some keywords)
- ⚠️ API errors - Check SerpAPI key
- ⚠️ Google Docs/Sheets errors - Check credentials file

---

## 🐛 Troubleshooting Tests

### Test 1: Check API Connection
```bash
python3 main.py -u https://www.google.com -k "test"
```
- **If error:** Check SerpAPI key in `.env`
- **If success:** API is working

### Test 2: Check Google Docs/Sheets Connection
```bash
python3 setup.py
```
- **Should show:** Google Docs/Sheets credentials status
- **If missing:** Download from Google Cloud Console (see GOOGLE_DOCS_SETUP.md)

### Test 3: Check Web Server
```bash
curl http://localhost:8080
```
- **If HTML returned:** Server is working
- **If error:** Check if server is running

---

## 📊 Expected Results Format

### Successful Result:
```
✅ google: Position 1 - https://www.google.com
   Title: Google
   Snippet: Search the world's information...
   Checked on: 2025-11-18 23:00:00
```

### Not Found Result:
```
⚠️  random keyword: > 100 - Not found in top 100
   Checked on: 2025-11-18 23:00:00
```

### Error Result:
```
❌ keyword: Error - API key invalid
```

---

## 🎯 Real-World Testing Scenarios

### Scenario 1: Track Your Own Website
1. Enter your website URL
2. Add keywords you want to rank for
3. Check rankings
4. Review results
5. Check again later to see changes

### Scenario 2: Competitor Analysis
1. Enter competitor's website
2. Add industry keywords
3. See where they rank
4. Compare with your rankings

### Scenario 3: Keyword Research
1. Test different keyword variations
2. See which ones your site ranks for
3. Identify opportunities

---

## 💡 Pro Tips

1. **Start Simple:** Test with well-known sites first (Google, Wikipedia)
2. **Use Brand Names:** Easier to verify results
3. **Test Multiple Keywords:** See how system handles bulk checks
4. **Check History:** Verify data is being saved
5. **Try Different Locations:** Test location parameter

---

## 🚀 Quick Test Commands

```bash
# Test 1: Simple single keyword
python3 main.py -u https://www.google.com -k "google"

# Test 2: Multiple keywords
python3 main.py -u https://www.wikipedia.org -k "wikipedia" "encyclopedia" "knowledge"

# Test 3: From CSV
python3 main.py -u https://www.example.com -f keywords_example.csv

# Test 4: Different location
python3 main.py -u https://www.google.com -k "google" --location "United Kingdom"

# Test 5: Start web interface
python3 app.py 8080
```

---

## ✅ Testing Checklist

- [ ] Server starts successfully
- [ ] Web interface loads at http://localhost:8080
- [ ] Can enter website URL
- [ ] Can enter keywords
- [ ] Form submission works
- [ ] Results display correctly
- [ ] Results are saved (check Google Docs/Sheets)
- [ ] History loads correctly
- [ ] CSV upload works
- [ ] Multiple keywords work
- [ ] Error handling works (try invalid URL)

---

## 🎓 Example Test Session

```bash
# 1. Start server
python3 app.py 8080

# 2. In browser, go to http://localhost:8080

# 3. Enter:
#    Website: https://www.google.com
#    Keywords:
#      google
#      search engine
#      web browser

# 4. Click "Check Rankings"

# 5. Expected results:
#    ✅ google: Position 1
#    ✅ search engine: Position 1
#    ✅ web browser: Position 1-3

# 6. Check History section
#    Should show the checks you just made
```

---

## 🆘 If Tests Fail

### API Errors:
- Check SerpAPI key in `.env`
- Verify API quota/limits
- Test API key directly

### Google Docs/Sheets Errors:
- Check `credentials.json` exists
- Verify Google Docs API or Sheets API is enabled
- Check Document ID or Spreadsheet ID in `.env`

### Server Errors:
- Check port is available
- Try different port: `python3 app.py 3000`
- Check for Python errors

### No Results:
- Normal if website doesn't rank for keyword
- Try different keywords
- Check if website is indexed by Google

---

**Ready to test? Start with a simple test using Google's website and the keyword "google" - it should show Position 1!**


