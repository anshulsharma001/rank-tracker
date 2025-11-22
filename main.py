"""
Main Application Script
Google Rank Tracking System - Automated keyword ranking checker
"""
import sys
import argparse
import csv
from typing import List
from rank_checker import RankChecker
import config

# Import storage manager based on configuration
if config.STORAGE_TYPE == 'docs':
    from google_docs_manager import GoogleDocsManager
    StorageManager = GoogleDocsManager
elif config.STORAGE_TYPE == 'sheets':
    from google_sheets_manager import GoogleSheetsManager
    StorageManager = GoogleSheetsManager
else:
    # Default to Google Docs
    from google_docs_manager import GoogleDocsManager
    StorageManager = GoogleDocsManager


def load_keywords_from_csv(csv_file: str) -> List[str]:
    """
    Load keywords from a CSV file
    
    Args:
        csv_file: Path to CSV file
        
    Returns:
        List of keywords
    """
    keywords = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0].strip():  # Skip empty rows
                    keywords.append(row[0].strip())
        return keywords
    except FileNotFoundError:
        print(f"Error: CSV file not found: {csv_file}")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []


def run_rank_tracking(url: str, keywords: List[str], location: str = "United States", sheet_name: str = "Rank Tracking"):
    """
    Core function to run rank tracking (can be called directly or via CLI)
    
    Args:
        url: Website URL to track
        keywords: List of keywords to check
        location: Search location
        sheet_name: Google Sheets sheet name
        
    Returns:
        List of ranking result dictionaries
    """
    print(f"\n{'='*60}")
    print("Google Rank Tracking System")
    print(f"{'='*60}")
    print(f"Website URL: {url}")
    print(f"Keywords to check: {len(keywords)}")
    print(f"Location: {location}")
    print(f"{'='*60}\n")
    
    # Initialize rank checker
    try:
        rank_checker = RankChecker()
    except ValueError as e:
        print(f"Error: {e}")
        return []
    
    # Check rankings
    print("Starting rank checks...\n")
    results = rank_checker.check_multiple_keywords(
        keywords, 
        url, 
        location
    )
    
    # Display results
    print(f"\n{'='*60}")
    print("Ranking Results:")
    print(f"{'='*60}")
    for result in results:
        pos = result['ranking_position']
        keyword = result['keyword']
        found_url = result['found_url']
        
        if result.get('error'):
            print(f"❌ {keyword}: Error - {result['error']}")
        elif isinstance(pos, int) or (isinstance(pos, str) and not pos.startswith('>')):
            print(f"✅ {keyword}: Position {pos} - {found_url}")
        else:
            print(f"⚠️  {keyword}: {pos} - Not found in top 100")
    
    # Save results to storage
    print(f"\n{'='*60}")
    if config.STORAGE_TYPE == 'docs':
        print("Saving results to Google Docs...")
    else:
        print("Saving results to Google Sheets...")
    print(f"{'='*60}")
    
    try:
        storage_manager = StorageManager()
        if config.STORAGE_TYPE == 'docs':
            storage_manager.append_results(results)
        else:
            storage_manager.append_results(results, sheet_name)
        print("✅ Results saved successfully!")
    except Exception as e:
        print(f"❌ Error saving results: {e}")
        print("Results are still available in the console output above.")
    
    print(f"\n{'='*60}")
    print("Rank tracking completed!")
    print(f"{'='*60}\n")
    
    return results


def main():
    """Main function to run the rank tracking system via CLI"""
    parser = argparse.ArgumentParser(
        description='Automated Google Rank Tracking System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single keyword
  python main.py -u https://www.example.com -k "artificial intelligence tools"
  
  # Multiple keywords
  python main.py -u https://www.example.com -k "AI software" "best AI companies"
  
  # From CSV file
  python main.py -u https://www.example.com -f keywords.csv
  
  # Custom location
  python main.py -u https://www.example.com -k "AI tools" --location "United Kingdom"
        """
    )
    
    parser.add_argument('-u', '--url', required=True,
                       help='Website URL to track (e.g., https://www.example.com)')
    parser.add_argument('-k', '--keywords', nargs='+',
                       help='One or more keywords to check')
    parser.add_argument('-f', '--file',
                       help='CSV file containing keywords (one per line)')
    parser.add_argument('--location', default='United States',
                       help='Search location (default: United States)')
    parser.add_argument('--sheet-name', default='Rank Tracking',
                       help='Google Sheets sheet name (default: Rank Tracking)')
    
    args = parser.parse_args()
    
    # Get keywords
    keywords = []
    if args.file:
        keywords = load_keywords_from_csv(args.file)
        if not keywords:
            print("No keywords found in CSV file")
            sys.exit(1)
    elif args.keywords:
        keywords = args.keywords
    else:
        print("Error: Either --keywords or --file must be provided")
        sys.exit(1)
    
    # Run rank tracking
    run_rank_tracking(args.url, keywords, args.location, args.sheet_name)


if __name__ == '__main__':
    main()

