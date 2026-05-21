# 📊 MCP CSV Analyst

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/ChenneyZhuang/mcp-csv-analyst/actions/workflows/ci.yml/badge.svg)](https://github.com/ChenneyZhuang/mcp-csv-analyst/actions/workflows/ci.yml)

**MCP server for CSV data analysis — stats, charts, and AI-powered insights.**

Drop a CSV file → your AI agent gets full statistical analysis, visualizations,
and LLM-generated insights.

---

## Quick Start

```bash
pip install git+https://github.com/ChenneyZhuang/mcp-csv-analyst.git
```

For AI-powered insights, set your API key:
```bash
export DEEPSEEK_API_KEY="***"
```

### Claude Desktop

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

### Claude Code

```bash
claude mcp add csv-analyst python3 -m mcp_csv_analyst.server
```

---

## Tools

| Tool | Description |
|------|-------------|
| `csv_stats(file_path)` | Statistical summaries (mean, median, std, correlations) |
| `csv_charts(file_path, output_dir)` | Generate histogram, box plot, heatmap, bar charts |
| `csv_analyze(file_path)` | Full analysis — stats + charts + AI insights |

---

## vs pandas-mcp-server

| | This Server | pandas-mcp-server |
|---|:--:|:--:|
| Statistical summary | ✅ Automatic | ❌ Manual code |
| AI-powered insights | ✅ Built-in | ❌ |
| Correlation matrix | ✅ | ❌ |
| Charts | ✅ PNG | ✅ HTML |
| Requires coding | ❌ No | ✅ Write pandas code |

---

## License

MIT
