---
name: sec-filing-monitor
description: Monitor SEC filings for specified companies. Checks today's feed and the latest filing for context. Requires user identity.
---

# SEC Filing Monitor Skill

## Usage
`python3 monitor.py TICKER1 TICKER2 ... --identity "Your Name email@example.com"`

Example:
`python3 skills/sec-filing-monitor/monitor.py AAPL BABA TSLA --identity "Kelvin kelvin@example.com"`

## Output
- Checks today's SEC feed for new filings.
- Lists the latest filing date for each ticker as context.
