FROM python:3.12-slim
WORKDIR /app
COPY *.py ./
COPY agent ./agent
COPY demo ./demo
COPY docs ./docs
COPY samples ./samples
ENV HOST=0.0.0.0 PYTHONUNBUFFERED=1
CMD ["python3", "server.py"]
