"""MCP server for CSV data analysis with AI-powered insights."""

import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CSV Analyst")


@mcp.tool()
def csv_stats(file_path: str) -> dict:
    """Compute statistical summaries for a CSV file.

    Returns column types, basic stats (mean, median, std, min, max),
    missing value counts, and skewness/kurtosis for numeric columns.
    """
    from csv_analyst.tools.stats import compute_stats, compute_correlations

    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        return {"error": f"File not found: {file_path}"}
    if path.suffix.lower() != ".csv":
        return {"error": "Only CSV files supported"}

    stats = compute_stats(str(path))
    correlations = compute_correlations(str(path))

    return {
        "file": str(path),
        "rows": stats.row_count,
        "columns": stats.column_count,
        "column_stats": [
            {
                "name": c.name,
                "dtype": c.dtype,
                "missing": c.missing_count,
                "missing_pct": round(c.missing_pct, 2),
                "mean": c.mean,
                "median": c.median,
                "std": c.std,
                "min": c.min_val,
                "max": c.max_val,
                "skewness": c.skewness,
                "kurtosis": c.kurtosis,
            }
            for c in stats.columns
        ],
        "correlations": correlations,
    }


@mcp.tool()
def csv_charts(file_path: str, output_dir: str = "./charts") -> dict:
    """Generate charts for a CSV file.

    Produces histogram, box plot, correlation heatmap, and bar charts
    for categorical columns. Returns paths to generated PNG files.
    """
    from csv_analyst.tools.charts import generate_charts

    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        return {"error": f"File not found: {file_path}"}

    out = Path(output_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    chart_paths = generate_charts(str(path), str(out))

    return {
        "file": str(path),
        "charts": [str(p) for p in chart_paths],
        "output_dir": str(out),
    }


@mcp.tool()
def csv_analyze(file_path: str) -> dict:
    """Full analysis of a CSV file — stats + AI-powered insights.

    Computes statistics, generates charts, and uses an LLM to produce
    human-readable insights about patterns, outliers, and recommendations.
    Requires DEEPSEEK_API_KEY environment variable for AI analysis.
    """
    import os
    from csv_analyst.pipeline import AnalysisPipeline

    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        return {"error": f"File not found: {file_path}"}

    pipeline = AnalysisPipeline()
    result = pipeline.run(str(path))

    return {
        "file": str(path),
        "rows": result.stats.row_count,
        "columns": result.stats.column_count,
        "highlights": result.highlights,
        "insights": result.insights,
        "charts": [str(p) for p in result.chart_paths],
        "ai_analysis_available": bool(os.getenv("DEEPSEEK_API_KEY")),
    }


def main():
    mcp.run()


if __name__ == "__main__":
    main()
