FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=news_platform.settings.dev
ENV SECRET_KEY=change-me-docker-dev-key-at-least-50-characters-long
ENV DEBUG=True
ENV ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
