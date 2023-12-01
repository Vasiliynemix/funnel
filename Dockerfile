# Используем базовый образ Python 3.11
FROM python:3.11

RUN apt-get update && apt-get install -y netcat-openbsd

RUN apt-get update && apt-get install -y postgresql-client

# Создаем директорию для приложения
WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry

# Копируем файлы pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock /app/

# Настройка Poetry
RUN poetry config virtualenvs.create false

# Устанавливаем зависимости
RUN poetry install --no-interaction --no-ansi --no-dev || cat /app/pyproject.toml

# Копируем все остальные файлы в контейнер
COPY . /app/

RUN chmod a+x docker/*.sh