# How to Use - Check Website Ranking Positions

## What This System Does

This system helps you find **where your website ranks** on Google Search for specific keywords.

### Example Scenario:
- **Your website:** `https://www.example.com`
- **Keyword:** "artificial intelligence tools"
- **Question:** "Where does my website appear when someone searches for 'artificial intelligence tools'?"

**Answer:** The system will tell you:
- ✅ **Position 4** - Your website is at position 4 in Google search results
- ⚠️ **> 100** - Your website is not in the top 100 results
- ❌ **Error** - Something went wrong (API issue, etc.)

---

## Quick Start

### Step 1: Prepare Your Information

You need:
1. **Website URL** - The website you want to track (e.g., `https://www.example.com`)
2. **Keywords** - What people search for (e.g., "AI tools", "machine learning")

### Step 2: Run the Check

#### Option A: Single Keyword
```bash
python3 main.py -u https://www.example.com -k "artificial intelligence tools"
```

**Output:**
```
✅ artificial intelligence tools: Position 4 - https://www.example.com/ai-tools
```

#### Option B: Multiple Keywords
```bash
python3 main.py -u https://www.example.com -k "AI software" "best AI companies" "machine learning"
```

**Output:**
```
✅ AI software: Position 12 - https://www.example.com/software
✅ best AI companies: Position 3 - https://www.example.com/companies
⚠️  machine learning: > 100 - Not found in top 100
```

#### Option C: From CSV File
```bash
python3 main.py -u https://www.example.com -f keywords_example.csv
```

---

## Understanding the Results

### Position Numbers
- **Position 1-100**: Your website was found at that position
  - Position 1 = First result (top of page 1)
  - Position 10 = Last result on page 1
  - Position 11 = First result on page 2
  - Position 100 = Last result on page 10

### Status Indicators
- ✅ **Green checkmark**: Website found in search results
- ⚠️ **Warning**: Website not found in top 100 results
- ❌ **Error**: Something went wrong (check API keys, network, etc.)

### Example Output
```
============================================================
Ranking Results:
============================================================
✅ artificial intelligence tools: Position 4 - https://www.example.com/ai-tools
✅ AI software: Position 12 - https://www.example.com/software
⚠️  best AI companies: > 100 - Not found in top 100
✅ machine learning platforms: Position 8 - https://www.example.com/platforms
```

---

## Real-World Examples

### Example 1: Check Your Blog's Ranking
```bash
python3 main.py -u https://myblog.com -k "python tutorials" "web development"
```

**Result:** See where your blog appears when people search for these topics.

### Example 2: Track Competitor Rankings
```bash
python3 main.py -u https://competitor.com -k "best software" "top companies"
```

**Result:** See where your competitor ranks for important keywords.

### Example 3: Monitor Multiple Pages
```bash
# Check homepage
python3 main.py -u https://example.com -k "company name"

# Check product page
python3 main.py -u https://example.com/products -k "product name"
```

---

## What Gets Saved

Every check is automatically saved to Google Docs/Google Sheets with:
- Keyword searched
- Website URL checked
- Ranking position found
- Date and time of check
- The actual URL that appeared in results
- SERP title and snippet

This lets you:
- Track ranking changes over time
- See historical data
- Analyze trends
- Compare different keywords

---

## Advanced Usage

### Custom Location
Check rankings for a specific country:
```bash
python3 main.py -u https://www.example.com -k "keyword" --location "United Kingdom"
```

### Scheduled Checks
Run automatic checks daily:
```bash
python3 scheduler.py -u https://www.example.com -k "keyword" --daily 09:00
```

This will check rankings every day at 9 AM and save results automatically.

---

## Common Questions

### Q: What if my website doesn't appear?
**A:** You'll see "> 100" which means your website is not in the top 100 search results. Try:
- Different keyword variations
- More specific keywords
- Check if your website is actually indexed by Google

### Q: Can I check multiple websites?
**A:** Yes! Run the command multiple times with different URLs:
```bash
python3 main.py -u https://website1.com -k "keyword"
python3 main.py -u https://website2.com -k "keyword"
```

### Q: How accurate are the results?
**A:** Results are based on Google's actual search results via SerpAPI. They reflect what users see when searching.

### Q: Can I check rankings for different countries?
**A:** Yes! Use the `--location` parameter:
```bash
python3 main.py -u https://www.example.com -k "keyword" --location "India"
```

---

## Next Steps

1. **Set up Google Docs** (if not done) - See `GOOGLE_DOCS_SETUP.md`
2. **Run your first check** - Use the examples above
3. **Schedule regular checks** - Use the scheduler for automatic tracking
4. **Analyze results** - View data in Google Docs or Google Sheets

---

## Need Help?

- Check `README.md` for full documentation
- Run `python3 setup.py` to verify your setup
- Make sure your SerpAPI key is configured in `.env`


