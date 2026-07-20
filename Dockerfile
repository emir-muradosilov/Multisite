FROM python:3.12-slim

# Создаём непривилегированного пользователя
RUN useradd -ms /bin/bash django

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY --chown=django:django . .

# Копируем entrypoint и даём права
COPY --chown=django:django entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Переключаемся на пользователя django
USER django

ENTRYPOINT ["/entrypoint.sh"]