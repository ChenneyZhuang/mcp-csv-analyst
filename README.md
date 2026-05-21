# MCP CSV Analyst

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/ChenneyZhuang/mcp-csv-analyst/actions/workflows/ci.yml/badge.svg)](https://github.com/ChenneyZhuang/mcp-csv-analyst/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/ChenneyZhuang/mcp-csv-analyst)](https://github.com/ChenneyZhuang/mcp-csv-analyst/releases)

**Drop a CSV file. Your AI agent becomes a data analyst.**

Automatic descriptive statistics, correlation matrices, 8 chart types, anomaly detection, and optional AI-powered narrative insights — no pandas knowledge required. The agent calls a tool, the server does the math.

---

## Why This One?

Most CSV MCP servers make you **write pandas code manually** through the agent. This server computes everything automatically — and optionally adds LLM-generated insights on top.

| | This Server | `pandas-mcp-server` | `csv-mcp-server` |
|---|:---:|:---:|:---:|
| Automatic statistics | ✅ | ❌ (manual code) | ❌ |
| AI-powered insights | ✅ built-in | ❌ | ❌ |
| Correlation matrix | ✅ | ❌ | ❌ |
| Charts (PNG) | ✅ 8 types | ✅ (HTML/JS) | ❌ |
| Skewness / kurtosis | ✅ | ❌ | ❌ |
| Anomaly detection | ✅ | ❌ | ❌ |
| Requires pandas knowledge | ❌ | ✅ | ✅ |

---

## Installation

```bash
pip install git+https://github.com/ChenneyZhuang/mcp-csv-analyst.git
```

For AI-powered insights (optional):

```bash
export DEEPSEEK_API_KEY="your-key-here"
```

Works with any OpenAI-compatible endpoint — set `DEEPSEEK_BASE_URL` to switch providers. Without an API key, all tools work in offline mode (stats + charts only).

### Docker

```bash
docker build -t mcp-csv-analyst github.com/ChenneyZhuang/mcp-csv-analyst
docker run -i -e DEEPSEEK_API_KEY=sk-... mcp-csv-analyst
```

---

## Configuration

### Claude Desktop

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

Compute comprehensive statistics for every column.

**Parameter:** `file_path` (str) — path to CSV

```json
{
  "file": "/data/sales.csv",
  "rows": 15000,
  "columns": 8,
  "numeric_stats": [
    {
      "column": "revenue",
      "count": 14977,
      "mean": 45230.5,
      "median": 38100.0,
      "std": 12450.3,
      "min": 1200.0,
      "max": 98500.0,
      "skewness": 1.23,
      "kurtosis": 2.89
    }
  ],
  "categorical_stats": [
    {
      "column": "region",
      "unique_count": 5,
      "top_value": "North",
      "top_freq": 4521,
      "top_pct": 30.1
    }
  ],
  "column_info": [
    {
      "name": "revenue",
      "dtype": "float64",
      "inferred_type": "numeric",
      "null_count": 23,
      "null_pct": 0.15
    }
  ],
  "correlations": {
    "revenue": {"customers": 0.87, "marketing_spend": 0.64}
  }
}
```

### `csv_charts`

Generate charts from CSV data.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file_path` | `str` | *(required)* | Path to CSV |
| `output_dir` | `str` | `"./charts"` | Where to save PNGs |

```json
{
  "file": "/data/sales.csv",
  "charts": [
    {"title": "Histogram: revenue", "path": "/charts/hist_revenue.png", "description": "Distribution of revenue"},
    {"title": "Box Plot: revenue", "path": "/charts/box_revenue.png", "description": "Outlier detection for revenue"},
    {"title": "Correlation Heatmap", "path": "/charts/correlation_heatmap.png", "description": "Numeric column correlations"},
    {"title": "Bar Chart: region", "path": "/charts/bar_region.png", "description": "Top categories for region"}
  ],
  "output_dir": "/charts"
}
```

8 chart types: histogram, box plot, correlation heatmap, bar chart, missing values visualization, and more. All rendered as 150 DPI PNGs.

### `csv_analyze`

Full pipeline — stats + charts + anomaly detection + AI insights in one call.

**Parameter:** `file_path` (str) — path to CSV

```json
{
  "file": "/data/sales.csv",
  "rows": 15000,
  "columns": 8,
  "numeric_columns": 4,
  "categorical_columns": 4,
  "anomalies": [
    {
      "column": "revenue",
      "value": "98500.0",
      "reason": "Value is 3.5 standard deviations above the mean",
      "severity": "warning"
    }
  ],
  "charts": [
    {"title": "Histogram: revenue", "path": "/charts/hist_revenue.png"}
  ],
  "ai_analysis_available": true,
  "insights": {
    "summary": "Revenue shows a clear upward trend in Q4...",
    "key_insights": ["Revenue is right-skewed", "Strong correlation with customers (0.87)"],
    "correlations_noted": ["revenue ↔ customers: 0.87"],
    "data_quality_notes": ["23 missing values in revenue (0.15%)"],
    "recommendations": ["Consider imputing missing revenue values"]
  }
}
```

Without `DEEPSEEK_API_KEY`, the `insights` field is omitted — statistics, charts, and anomaly detection always work offline.

---

## Usage Examples

### Quick stats check

```
User: "What's in this sales.csv?"
Agent: calls csv_stats("/path/to/sales.csv")
       → returns 8 columns, 15K rows, revenue right-skewed
Agent: "Your sales data has 8 columns and 15,000 rows.
       Revenue is right-skewed — consider using median for averages."
```

### Deep analysis with charts

```
User: "Analyze sales.csv and show me the patterns."
Agent: calls csv_analyze("/path/to/sales.csv")
       → stats + 8 charts + AI narrative
Agent: "Revenue peaks in Q4. Customer count and revenue are
       strongly correlated (0.87). Charts generated showing
       the seasonal pattern."
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

Three engines, one server:

1. **Stats** (`pandas` + `scipy`): descriptive statistics, skewness, kurtosis, Pearson correlation
2. **Charts** (`matplotlib`): histogram, box plot, heatmap, bar charts at 150 DPI
3. **AI** (DeepSeek / OpenAI-compatible, optional): receives aggregated statistics only — never raw data — and produces narrative insights

---

## AI Analysis (Optional)

Set `DEEPSEEK_API_KEY` to enable LLM-powered insights via `csv_analyze`. The LLM receives structured statistics (means, correlations, anomalies) — never raw rows.

| Variable | Default | Description |
|----------|---------|-------------|
| `DEEPSEEK_API_KEY` | *(required for AI)* | Your API key |
| `DEEPSEEK_BASE_URL` | `https://api.deepseek.com/v1` | Override for any OpenAI-compatible endpoint |
| `DEEPSEEK_MODEL` | `deepseek-chat` | Model name |
| `DEEPSEEK_MAX_TOKENS` | `4096` | Max response tokens |

---

## FAQ

**How large a CSV can it handle?**
Tested up to 100K rows × 20 columns. For larger files, consider sampling.

**Does it modify my data?**
No. All tools are read-only. Your CSV files are never touched.

**Is my data sent to external APIs?**
Only if you set `DEEPSEEK_API_KEY` and call `csv_analyze`. Even then, only aggregated statistics are sent — never raw rows. `csv_stats` and `csv_charts` are fully offline.

**Can I use OpenAI instead of DeepSeek?**
Yes. Set `DEEPSEEK_BASE_URL=https://api.openai.com/v1` and `DEEPSEEK_MODEL=gpt-4o`. Any OpenAI-compatible endpoint works.

---

## Related

- [csv-analyst-agent](https://github.com/ChenneyZhuang/csv-analyst-agent) — the underlying analysis library (CLI + Python API)
- [pandas-mcp-server](https://github.com/marlonluo2018/pandas-mcp-server) — alternative: requires writing pandas code manually
- [Model Context Protocol](https://modelcontextprotocol.io) — MCP specification

## License

MIT
