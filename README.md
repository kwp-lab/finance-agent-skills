# fetch-financial-reports

Fetch SEC XBRL financial data and save to local files for analysis.

## Usage

```bash
python fetch_xbrl.py AAPL                # Apple 10-K → output/AAPL/
python fetch_xbrl.py MSFT --form 10-Q    # Microsoft 10-Q
python fetch_xbrl.py NVDA -f 10-Q -o ./data  # Custom output
```

## Dependencies

```bash
pip install edgartools
```

## Output

Files saved to `output/<TICKER>/`:
- Full markdown report with all financial statements
- Individual statement files (income, balance sheet, cash flow)
- Metadata JSON with filing info
