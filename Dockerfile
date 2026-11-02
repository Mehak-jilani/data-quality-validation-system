FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY pipeline.py config.yaml ./
COPY bank.csv ./
CMD ["python", "pipeline.py", "--input", "bank.csv", "--config", "config.yaml"]
