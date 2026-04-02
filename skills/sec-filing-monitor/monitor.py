import argparse
from datetime import datetime, date
from edgar import set_identity, get_current_filings, Company

def main():
    parser = argparse.ArgumentParser(description="Check for new SEC filings for specified tickers.")
    parser.add_argument("tickers", nargs="+", help="Tickers to check (e.g., AAPL TSLA)")
    parser.add_argument("--identity", "-i", required=True, help="User Identity for SEC EDGAR (e.g., 'Name email@domain.com')")
    args = parser.parse_args()
    
    set_identity(args.identity)
    
    tickers = [t.upper() for t in args.tickers]
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking filings for: {', '.join(tickers)}")
    
    # 1. Check Today's Filings via get_current_filings()
    # This fetches the latest stream (usually current day)
    print("\n--- Scanning Today's SEC Feed ---")
    try:
        current = get_current_filings()
        found_today = False
        for t in tickers:
            matches = current.filter(ticker=t)
            if matches:
                found_today = True
                print(f"🚨 NEW FILING FOUND FOR {t}:")
                for m in matches:
                    print(f"   - Form: {m.form}")
                    print(f"   - Date: {m.filing_date}")
                    print(f"   - Link: {m.homepage_url}")
            else:
                pass # Silent if nothing today
        
        if not found_today:
            print("✅ No new filings found in today's feed for these companies.")
            
    except Exception as e:
        print(f"⚠️ Error scanning feed: {e}")

    # 2. Check Latest Filing for Each Company (Context)
    print("\n--- Latest Filing Status (Context) ---")
    for t in tickers:
        try:
            company = Company(t)
            latest = company.get_filings().latest()
            if latest:
                f_date = latest.filing_date
                # edgartools usually returns a string YYYY-MM-DD for filing_date, but sometimes it might be a date object depending on version.
                # Let's handle both.
                if isinstance(f_date, str):
                    f_date_obj = datetime.strptime(f_date, "%Y-%m-%d").date()
                else:
                    f_date_obj = f_date
                
                print(f"📌 {t}: Last filing was {latest.form} on {f_date}")
                
                delta = (date.today() - f_date_obj).days
                if delta <= 3:
                     print(f"   🚨 (RECENT! {delta} days ago)")
                print(f"   Link: {latest.homepage_url}")
            else:
                print(f"📌 {t}: No filings found.")
        except Exception as e:
            print(f"⚠️ Could not fetch details for {t}: {e}")

if __name__ == "__main__":
    main()
