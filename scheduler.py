"""
Scheduler Module
Handles automated scheduling of rank checks
"""
import schedule
import time
import sys
from datetime import datetime
from main import run_rank_tracking
import argparse


def run_scheduled_check(url: str, keywords: list, location: str = "United States", sheet_name: str = "Rank Tracking"):
    """
    Wrapper function to run rank check with specific parameters
    
    Args:
        url: Website URL to track
        keywords: List of keywords
        location: Search location
        sheet_name: Google Sheets sheet name
    """
    print(f"\n[{datetime.now()}] Running scheduled rank check...")
    
    try:
        run_rank_tracking(url, keywords, location, sheet_name)
    except Exception as e:
        print(f"Error during scheduled check: {e}")


def main():
    """Main scheduler function"""
    parser = argparse.ArgumentParser(
        description='Schedule automated Google Rank Tracking',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Daily check at 9 AM
  python scheduler.py -u https://www.example.com -k "AI tools" --daily 09:00
  
  # Weekly check on Monday at 10 AM
  python scheduler.py -u https://www.example.com -k "AI tools" --weekly monday 10:00
  
  # Every 6 hours
  python scheduler.py -u https://www.example.com -k "AI tools" --hours 6
        """
    )
    
    parser.add_argument('-u', '--url', required=True,
                       help='Website URL to track')
    parser.add_argument('-k', '--keywords', nargs='+', required=True,
                       help='Keywords to check')
    parser.add_argument('--location', default='United States',
                       help='Search location')
    parser.add_argument('--sheet-name', default='Rank Tracking',
                       help='Google Sheets sheet name')
    
    # Scheduling options
    parser.add_argument('--daily', metavar='TIME',
                       help='Run daily at specified time (HH:MM format)')
    parser.add_argument('--weekly', nargs=2, metavar=('DAY', 'TIME'),
                       help='Run weekly on specified day and time')
    parser.add_argument('--hours', type=int,
                       help='Run every N hours')
    parser.add_argument('--minutes', type=int,
                       help='Run every N minutes')
    
    args = parser.parse_args()
    
    # Set up schedule
    if args.daily:
        schedule.every().day.at(args.daily).do(
            run_scheduled_check, 
            args.url, 
            args.keywords, 
            args.location, 
            args.sheet_name
        )
        print(f"Scheduled daily check at {args.daily}")
    
    elif args.weekly:
        day, time_str = args.weekly
        day_map = {
            'monday': schedule.every().monday,
            'tuesday': schedule.every().tuesday,
            'wednesday': schedule.every().wednesday,
            'thursday': schedule.every().thursday,
            'friday': schedule.every().friday,
            'saturday': schedule.every().saturday,
            'sunday': schedule.every().sunday
        }
        
        if day.lower() not in day_map:
            print(f"Error: Invalid day '{day}'. Use: monday, tuesday, wednesday, thursday, friday, saturday, sunday")
            sys.exit(1)
        
        day_map[day.lower()].at(time_str).do(
            run_scheduled_check,
            args.url,
            args.keywords,
            args.location,
            args.sheet_name
        )
        print(f"Scheduled weekly check on {day} at {time_str}")
    
    elif args.hours:
        schedule.every(args.hours).hours.do(
            run_scheduled_check,
            args.url,
            args.keywords,
            args.location,
            args.sheet_name
        )
        print(f"Scheduled check every {args.hours} hours")
    
    elif args.minutes:
        schedule.every(args.minutes).minutes.do(
            run_scheduled_check,
            args.url,
            args.keywords,
            args.location,
            args.sheet_name
        )
        print(f"Scheduled check every {args.minutes} minutes")
    
    else:
        print("Error: Must specify a schedule (--daily, --weekly, --hours, or --minutes)")
        sys.exit(1)
    
    # Run initial check
    print("\nRunning initial check...")
    run_scheduled_check(args.url, args.keywords, args.location, args.sheet_name)
    
    # Keep scheduler running
    print("\nScheduler running. Press Ctrl+C to stop.\n")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\nScheduler stopped.")


if __name__ == '__main__':
    main()

