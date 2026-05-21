"""MCP server for CSV data analysis with AI-powered insights."""

import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CSV Analyst")


@mcp.tool()
def csv_stats(file_path: str) -> dict:
    """Compute statistical summaries for a CSV file.

    Returns column types, basic stats (mean, median, std, min, max),
    missing value counts, and skewness/kurtosis for numeric columns.
    """
    from csv_analyst.tools import compute_stats_summary, compute_correlations
    from csv_analyst.tools.stats import profile_dataset

    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        return {"error": f"File not found: {file_path}"}
    if path.suffix.lower() != ".csv":
        return {"error": "Only CSV files supported"}

    profile = profile_dataset(str(path))
    stats = compute_stats_summary(str(path))
    correlations = compute_correlations(str(path))

    return {
        "file": str(path),
        "rows": profile.row_count,
        "columns": profile.column_count,
        "numeric_stats": [
            {
                "column": c.column,
                "count": c.count,
                "mean": c.mean,
                "median": c.median,
                "std": c.std,
                "min": c.min,
                "max": c.max,
                "skewness": c.skewness,
                "kurtosis": c.kurtosis,
            }
            for c in stats.numeric_stats
        ],
        "categorical_stats": [
            {
                "column": c.column,
                "unique_count": c.unique_count,
                "top_value": c.top_value,
                "top_freq": c.top_freq,
                "top_pct": c.top_pct,
            }
            for c in stats.categorical_stats
        ],
        "column_info": [
            {
                "name": c.name,
                "dtype": c.dtype,
                "inferred_type": c.inferred_type,
                "null_count": c.null_count,
                "null_pct": c.null_pct,
                "unique_count": c.unique_count,
            }
            for c in profile.columns
        ],
        "correlations": correlations,
    }


@mcp.tool()
def csv_charts(file_path: str, output_dir: str = "./charts") -> dict:
    """Generate charts for a CSV file.

    Produces histogram, box plot, correlation heatmap, and bar charts
    for categorical columns. Returns paths to generated PNG files.
    """
    from csv_analyst.tools import generate_all_charts

    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        return {"error": f"File not found: {file_path}"}

    out = Path(output_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    chart_refs = generate_all_charts(str(path), str(out))

    return {
        "file": str(path),
        "charts": [
            {"title": t, "path": str(p), "description": d}
            for t, p, d in chart_refs
        ],
        "output_dir": str(out),
    }


@mcp.tool()
def csv_analyze(file_path: str) -> dict:
    """Full analysis of a CSV file — stats + charts + AI-powered insights.

    Computes statistics, generates charts, and uses an LLM to produce
    human-readable insights about patterns, outliers, and recommendations.
    Requires DEEPSEEK_API_KEY environment variable for AI analysis.
    """
    from csv_analyst import AnalysisPipeline

    path = Path(file_path).expanduser().resolve()
    if not path.exists():
        return {"error": f"File not found: {file_path}"}

    pipeline = AnalysisPipeline()
    result = pipeline.run(str(path))

    response = {
        "file": str(path),
        "rows": result.profile.row_count,
        "columns": result.profile.column_count,
        "numeric_columns": len(result.stats.numeric_stats),
        "categorical_columns": len(result.stats.categorical_stats),
        "anomalies": [
            {
                "column": a.column,
                "value": a.value,
                "reason": a.reason,
                "severity": a.severity,
            }
            for a in result.anomalies.anomalies
        ],
        "charts": [
            {"title": c.title, "path": c.file_path}
            for c in result.charts
        ],
        "ai_analysis_available": bool(os.getenv("DEEPSEEK_API_KEY")),
    }

    if result.llm_analysis:
        response["insights"] = {
            "summary": result.llm_analysis.executive_summary,
            "key_insights": result.llm_analysis.key_insights,
            "correlations_noted": result.llm_analysis.correlations_noted,
            "data_quality_notes": result.llm_analysis.data_quality_notes,
            "recommendations": result.llm_analysis.recommendations,
        }

    return response


def main():
    mcp.run()


if __name__ == "__main__":
    main()
