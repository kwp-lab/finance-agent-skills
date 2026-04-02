# Finance Agent Skills

A collection of AI agent skills and agents for financial analysis, SEC filing retrieval, and company monitoring.

## Contents

### Skills (`skills/`)

| Skill | Description |
|-------|-------------|
| [fetch-financial-reports](./skills/fetch-financial-reports) | Fetch SEC 10-K/10-Q filings and extract XBRL financial data |
| [sec-edgar-skill](./skills/sec-edgar-skill) | Analyze SEC EDGAR filings using EdgarTools |
| [sec-filing-monitor](./skills/sec-filing-monitor) | Monitor SEC EDGAR for new filings from specific companies |

### Agents (`.buda/agents/`)

| Agent | Description |
|-------|-------------|
| [finance-analyst](./.buda/agents/finance-analyst) | A financial analysis agent bundling all three skills above |

## Repository

GitHub: [kwp-lab/finance-agent-skills](https://github.com/kwp-lab/finance-agent-skills)

## License

MIT
