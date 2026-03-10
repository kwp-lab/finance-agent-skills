---
name: fetch-financial-reports
description: Use this skill when users request SEC financial reports (10-K annual or 10-Q quarterly) for US-listed companies. Fetches and parses XBRL data with automatic fallback for foreign issuers.
---

# Fetch Financial Reports

Fetch and parse SEC financial filings for US-listed companies.

## When to Use
- User asks for annual report → 10-K
- User asks for quarterly report → 10-Q
- User mentions a stock ticker and wants financial data

## Workflow

### Step 1: Validate User Input
**Required inputs:**
- `ticker` - Stock symbol (e.g., AAPL, MSFT, BABA)
- `report_type` - Annual (10-K) or Quarterly (10-Q)

**If either is missing, ask the user:**
> "To fetch the financial report, I need:
> - **Ticker**: Which company? (e.g., AAPL, TSLA)
> - **Report Type**: Annual (10-K) or Quarterly (10-Q)?"

### Step 2: Execute Fetch
```bash
python fetch_xbrl.py <TICKER> -f <FORM> -o <WORKSPACE_ROOT>/financial_statements
```

| Report Type | US Companies | Foreign Issuers (ADR) |
|-------------|--------------|----------------------|
| Annual | 10-K | 20-F |
| Quarterly | 10-Q | 6-K |

### Step 3: Present Results
After successful fetch, present a **user-friendly summary**:

```
## <COMPANY_NAME> (<TICKER>) - <REPORT_TYPE> Report

### Key Highlights
- **Revenue**: $XXX billion (YoY: +X%)
- **Net Income**: $XXX billion
- **EPS**: $X.XX
- **Filing Date**: YYYY-MM-DD

### Financial Statements Available
- Income Statement
- Balance Sheet  
- Cash Flow Statement

📁 Full data saved to: `financial_statements/<TICKER>/<DATE>/`
```

### Step 4: Offer Next Actions
Always conclude with actionable options:

> **What would you like to do next?**
> 1. **Deep Analysis** - Analyze trends, ratios, and YoY comparisons
> 2. **Write Blog Post** - Draft a financial news article based on this report
> 3. **Download PDF** - Get the original SEC filing document

## Technical Details

### Output Location
`financial_statements/<TICKER>/<FILING_DATE>/`

Always use absolute path with `-o` flag: `workspace_root + /financial_statements`

### Output Files
**Primary (XBRL available):**
- `<FORM>_income_statement.txt`
- `<FORM>_balance_sheet.txt`
- `<FORM>_cash_flow_statement.txt`
- `<TICKER>_<FORM>_<DATE>.md` - Consolidated report

**Fallback (Entity Facts):**
- `<TICKER>_income_statement.txt`
- `<TICKER>_balance_sheet.txt`
- `<TICKER>_cash_flow_statement.txt`
- `<TICKER>_fallback_<DATE>.md` - Consolidated report
