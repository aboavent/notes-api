FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1         PYTHONUNBUFFERED=1         PIP_NO_CACHE_DIR=1

WORKDIR /app

# Create non-root user
RUN adduser --disabled-password --gecos "" app && chown -R app:app /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY app ./app
COPY pyproject.toml README.md ./

RUN mkdir -p /app/data && chown -R app:app /app
USER app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 CMD python -c "import socket,sys;s=socket.socket();s.settimeout(2);s.connect(('127.0.0.1',8000));s.close();sys.exit(0)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
