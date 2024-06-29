FROM python:3.12.3
WORKDIR image_store
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Settings logging
ENV LEVEL="DEBUG"
ENV GURU="True"
ENV TRACEBACK="False"

# Application settings
ENV APP_HOST=${HOST}
ENV APP_PORT=${PORT}

# Settings logging
ENV LEVEL="INFO"
ENV GURU="True"
ENV TRACEBACK="True"

# File settings
ENV SIZE=1048576

ENV S3_HOST="127.0.0.1"
ENV S3_PORT=8005


# Building
RUN pip install --upgrade pip  --no-cache-dir
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY image_store .

CMD python main.py