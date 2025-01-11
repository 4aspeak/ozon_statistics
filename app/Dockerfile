# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем Poetry
RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock ./


# Устанавливаем зависимости с помощью Poetry
RUN poetry config virtualenvs.create false && poetry install --no-root

# Копируем весь код приложения в контейнер
COPY . .

