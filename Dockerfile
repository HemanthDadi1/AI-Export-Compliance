FROM python:3.12-slim
WORKDIR /app
COPY *.py *.html ./
COPY demo ./demo
ENV HOST=0.0.0.0 PYTHONUNBUFFERED=1
CMD ["python3", "server.py"]
