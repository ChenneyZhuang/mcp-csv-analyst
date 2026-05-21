FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir git+https://github.com/ChenneyZhuang/mcp-csv-analyst.git

ENTRYPOINT ["python3", "-m", "mcp_csv_analyst.server"]
