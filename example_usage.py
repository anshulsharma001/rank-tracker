#!/usr/bin/env python3
"""
Example Usage Script
Demonstrates how to check website ranking positions
"""
from main import run_rank_tracking

# Example 1: Check a single keyword
print("=" * 60)
print("EXAMPLE 1: Single Keyword Check")
print("=" * 60)
print("Checking where 'example.com' ranks for 'artificial intelligence tools'")
print()

# Replace with your actual website URL
website_url = "https://www.example.com"
keywords = ["artificial intelligence tools"]

# This will:
# 1. Search Google for "artificial intelligence tools"
# 2. Find where example.com appears in the results
# 3. Report the position (e.g., Position 4, Position 15, or "> 100" if not found)
# 4. Save results to Google Docs/Google Sheets

# Uncomment to run:
# run_rank_tracking(website_url, keywords)

print("\n" + "=" * 60)
print("EXAMPLE 2: Multiple Keywords")
print("=" * 60)
print("Checking where 'example.com' ranks for multiple keywords")
print()

keywords = [
    "artificial intelligence tools",
    "AI software",
    "best AI companies",
    "machine learning platforms"
]

# This will check all keywords and show positions for each
# Uncomment to run:
# run_rank_tracking(website_url, keywords)

print("\n" + "=" * 60)
print("EXAMPLE 3: From CSV File")
print("=" * 60)
print("Checking rankings for keywords listed in keywords_example.csv")
print()

# You can also use a CSV file with keywords
# python3 main.py -u https://www.example.com -f keywords_example.csv

print("\n" + "=" * 60)
print("HOW IT WORKS:")
print("=" * 60)
print("""
1. You provide:
   - Website URL (e.g., https://www.example.com)
   - Keywords to check (e.g., "AI tools", "machine learning")

2. The system:
   - Searches Google for each keyword
   - Scans the top 100 search results
   - Finds where your website appears
   - Reports the position number

3. Results show:
   - ✅ Position 4 - Found at position 4
   - ⚠️  > 100 - Not found in top 100 results
   - ❌ Error - If there was an API error

4. All results are saved to Google Docs/Google Sheets for tracking
""")

print("\n" + "=" * 60)
print("QUICK START COMMANDS:")
print("=" * 60)
print("""
# Check single keyword:
python3 main.py -u https://www.example.com -k "your keyword"

# Check multiple keywords:
python3 main.py -u https://www.example.com -k "keyword1" "keyword2" "keyword3"

# Check from CSV file:
python3 main.py -u https://www.example.com -f keywords_example.csv

# Check with custom location:
python3 main.py -u https://www.example.com -k "keyword" --location "United Kingdom"
""")


