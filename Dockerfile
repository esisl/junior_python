# django-test/Dockerfile
FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Системные зависимости для psycopg2 и сборки
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src/ /app/

# Запуск через gunicorn (продакшн-рекомендация)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]