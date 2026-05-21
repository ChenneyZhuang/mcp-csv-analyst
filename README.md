# MCP CSV Analyst

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/ChenneyZhuang/mcp-csv-analyst/actions/workflows/ci.yml/badge.svg)](https://github.com/ChenneyZhuang/mcp-csv-analyst/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/ChenneyZhuang/mcp-csv-analyst)](https://github.com/ChenneyZhuang/mcp-csv-analyst/releases)

**MCP server for CSV data analysis — stats, charts, and AI-powered insights.**
Drop a CSV file and your AI agent becomes a data analyst: statistical summaries,
correlation matrices, visualizations, and LLM-generated narrative insights.

---

## Table of Contents

- [Why This One?](#why-this-one)
- [Installation](#installation)
- [Configuration](#configuration)
- [Tools](#tools)
  - [csv_stats](#csv_stats)
  - [csv_charts](#csv_charts)
  - [csv_analyze](#csv_analyze)
- [Usage Examples](#usage-examples)
- [How It Works](#how-it-works)
- [AI Analysis (Optional)](#ai-analysis-optional)
- [FAQ](#faq)
- [Related](#related)
- [License](#license)

---

## Why This One?

Most CSV MCP servers require you to **write pandas code manually**.
This server **computes everything automatically** — and optionally
adds AI-generated insights.

| | This Server | `pandas-mcp-server` | `csv-mcp-server` |
|---|---|:---:|:---:|
| Automatic statistics | ✅ | ❌ (manual code) | ❌ |
| AI-powered insights | ✅ built-in | ❌ | ❌ |
| Correlation matrix | ✅ | ❌ | ❌ |
| Charts (PNG) | ✅ histogram, box, heatmap, bar | ✅ (HTML/JS) | ❌ |
| Skewness / kurtosis | ✅ | ❌ | ❌ |
| Missing value analysis | ✅ | ❌ | ❌ |
| Requires pandas knowledge | ❌ no | ✅ yes | ✅ yes |

---

## Installation

```bash
pip install git+https://github.com/ChenneyZhuang/mcp-csv-analyst.git
```

For AI-powered insights (optional):
```bash
export DEEPSEEK_API_KEY="your-key-here"
```

Works with any OpenAI-compatible endpoint — set `DEEPSEEK_BASE_URL` to use
a different provider.

---

## Configuration

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "csv-analyst": {
      "command": "python3",
      "args": ["-m", "mcp_csv_analyst.server"],
      "env": {
        "DEEPSEEK_API_KEY": "your-key-here"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add csv-analyst --env DEEPSEEK_API_KEY=your-key python3 -m mcp_csv_analyst.server
```

### Cursor / Codex CLI

```json
{
  "mcpServers": {
    "csv-analyst": {
      "command": "python3",
      "args": ["-m", "mcp_csv_analyst.server"]
    }
  }
}
```

Set `DEEPSEEK_API_KEY` in your shell environment before launching.

---

## Tools

### `csv_stats`

Compute comprehensive statistics for every column in a CSV file.

**Parameters:**
- `file_path` (str) — path to the CSV file

**Returns:**
```json
{
  "file": "/Users/you/data/sales.csv",
  "rows": 15000,
  "columns": 8,
  "column_stats": [
    {
      "name": "revenue",
      "dtype": "float64",
      "missing": 23,
      "missing_pct": 0.15,
      "mean": 45230.5,
      "median": 38100.0,
      "std": 12450.3,
      "min": 1200.0,
      "max": 98500.0,
      "skewness": 1.23,
      "kurtosis": 2.89
    }
  ],
  "correlations": {
    "revenue": {"customers": 0.87, "marketing_spend": 0.64}
  }
}
```

Handles numeric, categorical, and datetime columns. Missing values are flagged
with counts and percentages.

### `csv_charts`

Generate publication-quality charts from CSV data.

**Parameters:**
- `file_path` (str) — path to the CSV file
- `output_dir` (str, default `"./charts"`) — where to save PNG files

**Returns:**
```json
{
  "file": "/Users/you/data/sales.csv",
  "charts": [
    "/Users/you/charts/revenue_histogram.png",
    "/Users/you/charts/revenue_boxplot.png",
    "/Users/you/charts/correlation_heatmap.png",
    "/Users/you/charts/category_bar.png"
  ],
  "output_dir": "/Users/you/charts"
}
```

Chart types: histogram (distribution), box plot (outliers), heatmap (correlations),
and bar chart (categorical breakdown). All rendered as 150 DPI PNGs.

### `csv_analyze`

Full pipeline — stats, charts, and AI insights in one call.

**Parameters:**
- `file_path` (str) — path to the CSV file

**Returns:**
```json
{
  "file": "/Users/you/data/sales.csv",
  "rows": 15000,
  "columns": 8,
  "highlights": [
    "Revenue is right-skewed (skewness: 1.23) — median is a better average than mean",
    "23 missing values in revenue (0.15%) — safe to drop or impute",
    "Strong correlation between revenue and customers (0.87)"
  ],
  "insights": "Revenue shows a clear upward trend in Q4, driven by...",
  "charts": ["/Users/you/charts/revenue_histogram.png", ...],
  "ai_analysis_available": true
}
```

Without `DEEPSEEK_API_KEY`, `highlights` contains statistical observations only
and `insights` returns an empty string. Charts are always generated.

---

## Usage Examples

### Quick stats check

```
User: "What's in this sales.csv?"
Agent: calls csv_stats("/path/to/sales.csv")
       → returns 8 columns, 15000 rows, revenue right-skewed
Agent: "Your sales data has 8 columns and 15000 rows. Revenue is
       right-skewed — consider using median for averages."
```

### Deep analysis with charts

```
User: "Analyze sales.csv and show me the patterns."
Agent: calls csv_analyze("/path/to/sales.csv")
       → stats + charts + AI narrative
Agent: "Revenue peaks in Q4 (Dec avg: $52K vs Jul avg: $31K).
       Customer count and revenue are strongly correlated (0.87).
       I've generated charts showing the seasonal pattern."
```

---

## How It Works

```
┌──────────┐     ┌──────────────┐     ┌────────────────┐
│ AI Agent │────▶│  MCP Server  │────▶│ csv_stats()    │
└──────────┘     │              │     │ csv_charts()   │
                 │              │     │ csv_analyze()  │
                 └──────────────┘     └───────┬────────┘
                                              │
                          ┌───────────────────┼───────────────────┐
                          ▼                   ▼                   ▼
                    ┌──────────┐       ┌──────────┐       ┌──────────┐
                    │  pandas  │       │matplotlib│       │ DeepSeek │
                    │  scipy   │       │  numpy   │       │  (opt)   │
                    └──────────┘       └──────────┘       └──────────┘
```

1. **Stats engine** (`pandas` + `scipy`): computes descriptive statistics,
   skewness, kurtosis, and Pearson correlation matrix for numeric columns.
2. **Chart engine** (`matplotlib`): generates histogram, box plot, heatmap,
   and bar charts as 150 DPI PNGs.
3. **AI interpreter** (`DeepSeek` / OpenAI-compatible, optional): takes the
   statistical output and produces human-readable narrative insights.

---

## AI Analysis (Optional)

Set `DEEPSEEK_API_KEY` to enable AI-powered insights via `csv_analyze`.
The LLM receives structured statistics (not raw data) and generates
narrative observations, trend analysis, and actionable recommendations.

**Environment variables:**
- `DEEPSEEK_API_KEY` — your API key (required for AI analysis)
- `DEEPSEEK_BASE_URL` — override for OpenAI-compatible proxies (default: `https://api.deepseek.com/v1`)
- `DEEPSEEK_MODEL` — model name (default: `deepseek-chat`)
- `DEEPSEEK_MAX_TOKENS` — max response tokens (default: `4096`)

Without an API key, all tools work in **offline mode** — statistics and charts
only, no AI narrative.

---

## FAQ

**How large a CSV can it handle?**
Tested up to 100K rows × 20 columns. For larger files, consider sampling
or using a dedicated data pipeline.

**What CSV formats are supported?**
Standard comma-separated CSV with headers. The parser auto-detects delimiters
and encodings for most common formats.

**Does it modify my data?**
No. All tools are read-only. Your CSV files are never modified.

**Is my data sent to DeepSeek?**
Only if you set `DEEPSEEK_API_KEY` AND call `csv_analyze`. Even then, only
**aggregated statistics** (means, correlations, etc.) are sent — never raw rows.
`csv_stats` and `csv_charts` never make network calls.

**Can I use OpenAI instead of DeepSeek?**
Yes. Set `DEEPSEEK_BASE_URL=https://api.openai.com/v1` and
`DEEPSEEK_MODEL=gpt-4o`. Any OpenAI-compatible endpoint works.

---

## Related

- [csv-analyst-agent](https://github.com/ChenneyZhuang/csv-analyst-agent) — the underlying analysis library (CLI + Python API)
- [pandas-mcp-server](https://github.com/marlonluo2018/pandas-mcp-server) — alternative: requires writing pandas code manually
- [Model Context Protocol](https://modelcontextprotocol.io) — MCP specification

## License

MIT
