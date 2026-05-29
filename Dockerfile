FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear directorios para archivos estáticos y media
RUN mkdir -p /app/staticfiles /app/media /app/media/exercise_images

# Recolectar archivos estáticos
RUN python manage.py collectstatic --noinput --clear

# Dar permisos amplios al directorio media para que Django pueda escribir
RUN chmod -R 777 /app/media

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

