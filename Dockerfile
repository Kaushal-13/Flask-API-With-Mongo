FROM python:3.9-slim
WORKDIR /app

RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5000


ENV FLASK_APP=App.py
ENV FLASK_RUN_HOST=0.0.0.0

# Start the Flask app
CMD ["python", "App.py"]
