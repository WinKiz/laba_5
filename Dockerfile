# 1. Базовый легковесный образ
FROM python:3.12-alpine

# 2. Указываем рабочую папку внутри контейнера
WORKDIR /app

# 3. Устанавливаем системные утилиты, необходимые для сборки пакетов
RUN apk add --no-cache gcc musl-dev postgresql-dev

# 4. Копируем файл зависимостей отдельно (для кэширования слоев Docker)
COPY app/requirements.txt .

# 5. Устанавливаем библиотеки Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Копируем весь остальной код приложения в контейнер
COPY app/ ./

# 7. Декларируем порт приложения
EXPOSE 8000

# 8. Команда запуска FastAPI при старте контейнера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]