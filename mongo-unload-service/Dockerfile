# pull uvicorn-gunicorn-fast-api-slim image that is optimised for performance
FROM tiangolo/uvicorn-gunicorn:python3.9-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MODULE_NAME=src.main
ENV PORT=8080
ENV LOG_LEVEL=debug
ENV PYTHONPATH=/app

RUN apt-get update
RUN apt-get install sqlite3

# for log file
RUN mkdir -p /opt/delphix/logs/

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./src /app/src
COPY table1_format.txt /app/
COPY test123.csv /app/

ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]


