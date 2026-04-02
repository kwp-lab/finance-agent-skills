# Finance Agent Skills

A collection of financial analysis and data monitoring skills for AI agents.
Turn your coding assistant into a financial analyst.

## Included Skills

| Skill | Description |
|-------|-------------|
| **[fetch-financial-reports](./fetch-financial-reports/SKILL.md)** | Fetch SEC 10-K/10-Q filings and extract XBRL financial data. |
| **[sec-filing-monitor](./sec-filing-monitor/SKILL.md)** | Monitor SEC EDGAR for new filings from specific companies. |
| **[sec-edgar-skill](./sec-edgar-skill/SKILL.md)** | Core utilities for interacting with the SEC EDGAR system. |

## Installation

You can install these skills using the [Agent Skills CLI](https://github.com/vercel-labs/skills).

### Install All Skills
Add the entire toolkit to your agent (OpenClaw, Claude Code, Cursor, etc.):

```bash
npx skills add kwp-lab/finance-agent-skills
```

### Install Specific Skills
If you only need a specific capability:

```bash
# Install only the report fetcher
npx skills add kwp-lab/finance-agent-skills --skill fetch-financial-reports

# Install only the monitor
npx skills add kwp-lab/finance-agent-skills --skill sec-filing-monitor
```

### Manual Installation
Clone this repository and symlink the skills to your agent's skill directory:

```bash
git clone https://github.com/kwp-lab/finance-agent-skills.git
cd finance-agent-skills

# Example for OpenClaw
ln -s $(pwd)/skills/fetch-financial-reports ~/.openclaw/skills/
ln -s $(pwd)/skills/sec-filing-monitor ~/.openclaw/skills/
```

## Requirements
Most skills in this package require Python 3.10+ and specific dependencies.
Check the `requirements.txt` inside each skill folder.

## License
MIT
