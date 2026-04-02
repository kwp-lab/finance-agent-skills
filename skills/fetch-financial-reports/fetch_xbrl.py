#!/usr/bin/env python3
"""
Fetch SEC XBRL financial data and save to local files.
Supports fallback to Entity Facts API when filing XBRL is missing.

Usage:
    python fetch_xbrl.py AAPL
    python fetch_xbrl.py BABA -f 6-K
"""

import os
import re
import json
import argparse
from datetime import datetime
from edgar import Company, set_identity

# SEC requires identification
set_identity("kagents agent@vikadata.com")

# Default output directory (relative to CWD)
DEFAULT_OUTPUT_DIR = "financial_statements"

# ANSI escape code pattern
ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    return ANSI_ESCAPE.sub('', text)


def ensure_output_dir(base_dir: str, subdir: str = None):
    """Create output directory if it doesn't exist."""
    path = base_dir
    if subdir:
        path = os.path.join(base_dir, subdir)
    os.makedirs(path, exist_ok=True)
    return path


def save_to_file(output_dir: str, filename: str, content: str, clean_ansi: bool = True):
    """Save content to a file in the output directory."""
    filepath = os.path.join(output_dir, filename)
    if clean_ansi:
        content = strip_ansi(content)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ Saved: {filepath}")
    return filepath


def fetch_financials_fallback(company, ticker: str, output_dir: str, date_str: str):
    """
    Fallback method: Fetch financials from Company Entity Facts (aggregated).
    Used when specific filing XBRL is missing.
    """
    print("\n⚠ XBRL missing in filing. Switching to Entity Facts (Fallback)...")
    print("=" * 80)
    
    # Create date subdirectory
    dated_output_dir = ensure_output_dir(output_dir, f"{ticker}/{date_str}")
    
    md_content = []
    md_content.append(f"# {company.name} Financials (Entity Facts Fallback)\n")
    md_content.append(f"**Ticker:** {ticker}  ")
    md_content.append(f"**CIK:** {company.cik}  ")
    md_content.append(f"**Source:** Entity Facts API (aggregated)  ")
    md_content.append(f"**Extracted At:** {datetime.now().isoformat()}\n")
    md_content.append("\n> Note: These data are from SEC Entity Facts (aggregated), not specific to one filing.\n")

    # Income Statement
    print("Fetching Income Statement (Entity Facts)...")
    try:
        income = company.income_statement()
        if income is not None:
            content = str(income)
            save_to_file(dated_output_dir, f"{ticker}_income_statement.txt", content)
            md_content.append("\n## Income Statement\n```\n" + content + "\n```\n")
    except Exception as e:
        print(f"  ✗ Failed: {e}")

    # Balance Sheet
    print("Fetching Balance Sheet (Entity Facts)...")
    try:
        balance = company.balance_sheet()
        if balance is not None:
            content = str(balance)
            save_to_file(dated_output_dir, f"{ticker}_balance_sheet.txt", content)
            md_content.append("\n## Balance Sheet\n```\n" + content + "\n```\n")
    except Exception as e:
        print(f"  ✗ Failed: {e}")

    # Cash Flow
    print("Fetching Cash Flow (Entity Facts)...")
    try:
        cash_flow = company.cash_flow_statement()
        if cash_flow is not None:
            content = str(cash_flow)
            save_to_file(dated_output_dir, f"{ticker}_cash_flow_statement.txt", content)
            md_content.append("\n## Cash Flow Statement\n```\n" + content + "\n```\n")
    except Exception as e:
        print(f"  ✗ Failed: {e}")

    # Save summary report
    report_filename = f"{ticker}_fallback_{date_str}.md"
    save_to_file(dated_output_dir, report_filename, "\n".join(md_content))
    print(f"\n✓ Fallback retrieval complete.")
    print(f"✓ Main report: {report_filename}")
    return dated_output_dir


def fetch_xbrl(ticker: str, form: str = "10-K", output_dir: str = None):
    """
    Fetch XBRL data for a given ticker and form type.
    """
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR
        
    form = form.upper()
    
    # Get company
    print(f"\nFetching {form} report for {ticker}...")
    print("=" * 80)
    
    try:
        company = Company(ticker)
        print(f"Company: {company.name}")
        print(f"CIK: {company.cik}")
    except Exception as e:
        print(f"✗ Error finding company {ticker}: {e}")
        return

    # Create output subdirectory (removed - now created inside XBRL/fallback logic)

    # Get latest filing
    filings = company.get_filings(form=form)
    latest_filing = None
    filing_date_str = datetime.now().strftime("%Y-%m-%d")  # Default to today
    
    if filings and len(filings) > 0:
        latest_filing = filings.latest()
        filing_date_str = str(latest_filing.filing_date)[:10]
        print(f"\nLatest {form} Filing:")
        print(f"  Date: {filing_date_str}")
        print(f"  Accession: {latest_filing.accession_number}")
    else:
        print(f"\n⚠ No {form} filings found. Will try fallback.")

    # Try Parsing XBRL
    xbrl_success = False
    ticker_output_dir = None
    
    if latest_filing:
        print("\nAttempting to parse XBRL from filing...")
        try:
            xbrl = latest_filing.xbrl()
            if xbrl:
                # Create date subdirectory: financial_statements/AAPL/2026-01-30/
                ticker_output_dir = ensure_output_dir(output_dir, f"{ticker}/{filing_date_str}")
                
                # Initialize markdown report
                md_content = []
                md_content.append(f"# {ticker} XBRL Financial Data ({form})\n")
                md_content.append(f"**Company:** {company.name}  ")
                md_content.append(f"**Ticker:** {ticker}  ")
                md_content.append(f"**CIK:** {company.cik}  ")
                md_content.append(f"**Form:** {form}  ")
                md_content.append(f"**Filing Date:** {filing_date_str}  ")
                md_content.append(f"**Accession Number:** {latest_filing.accession_number}  ")
                md_content.append(f"**Extracted At:** {datetime.now().isoformat()}\n")
                
                # XBRL Context
                xbrl_context = xbrl.to_context()
                md_content.append("\n## XBRL Context\n```")
                md_content.append(xbrl_context)
                md_content.append("```\n")
                
                statements = xbrl.statements
                
                # Income Statement
                if statements.income_statement():
                    content = str(statements.income_statement())
                    save_to_file(ticker_output_dir, f"{form}_income_statement.txt", content)
                    md_content.append("\n## Income Statement\n```")
                    md_content.append(content)
                    md_content.append("```\n")
                
                # Balance Sheet
                if statements.balance_sheet():
                    content = str(statements.balance_sheet())
                    save_to_file(ticker_output_dir, f"{form}_balance_sheet.txt", content)
                    md_content.append("\n## Balance Sheet\n```")
                    md_content.append(content)
                    md_content.append("```\n")
                
                # Cash Flow Statement
                if statements.cash_flow_statement():
                    content = str(statements.cash_flow_statement())
                    save_to_file(ticker_output_dir, f"{form}_cash_flow_statement.txt", content)
                    md_content.append("\n## Cash Flow Statement\n```")
                    md_content.append(content)
                    md_content.append("```\n")
                
                # Comprehensive Income
                if statements.comprehensive_income():
                    content = str(statements.comprehensive_income())
                    save_to_file(ticker_output_dir, f"{form}_comprehensive_income.txt", content)
                    md_content.append("\n## Comprehensive Income\n```")
                    md_content.append(content)
                    md_content.append("```\n")
                
                # Statement of Equity
                if statements.statement_of_equity():
                    content = str(statements.statement_of_equity())
                    save_to_file(ticker_output_dir, f"{form}_statement_of_equity.txt", content)
                    md_content.append("\n## Statement of Equity\n```")
                    md_content.append(content)
                    md_content.append("```\n")
                
                # Metadata
                metadata = {
                    "source": "filing_xbrl",
                    "company": company.name,
                    "ticker": ticker,
                    "cik": company.cik,
                    "form": form,
                    "filing_date": filing_date_str,
                    "accession_number": latest_filing.accession_number,
                    "extracted_at": datetime.now().isoformat()
                }
                save_to_file(ticker_output_dir, f"{form}_metadata.json", json.dumps(metadata, indent=2, ensure_ascii=False), clean_ansi=False)
                
                # Save full markdown report
                report_filename = f"{ticker}_{form}_{filing_date_str}.md"
                save_to_file(ticker_output_dir, report_filename, "\n".join(md_content))
                
                print("✓ XBRL extraction successful.")
                print(f"✓ Main report: {report_filename}")
                xbrl_success = True
            else:
                print("✗ Filing has no XBRL data.")
        except Exception as e:
            print(f"✗ XBRL parsing failed: {e}")

    # Fallback if XBRL failed
    if not xbrl_success:
        ticker_output_dir = fetch_financials_fallback(company, ticker, output_dir, filing_date_str)

    print("\n" + "=" * 80)
    print(f"✓ Data saved to: {ticker_output_dir}")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Fetch Financial Reports")
    parser.add_argument("ticker", nargs="?", default="AAPL", help="Ticker symbol")
    parser.add_argument("-f", "--form", choices=["10-K", "10-Q", "10-k", "10-q", "6-K", "6-k", "20-F", "20-f"], default="10-K", help="Form type")
    parser.add_argument("-o", "--output", default=None, help="Output directory")
    
    args = parser.parse_args()
    fetch_xbrl(args.ticker.upper(), args.form.upper(), args.output)


if __name__ == "__main__":
    main()
