import os
import time
import psycopg2
from fastapi import FastAPI

app = FastAPI()

# Получаем настройки подключения из переменных окружения
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")


def get_db_connection():
    # Пробуем подключиться к базе 10 раз с задержкой (чтобы СУБД успела стартовать)
    for _ in range(10):
        try:
            conn = psycopg2.connect(
                host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
            )
            return conn
        except psycopg2.OperationalError:
            time.sleep(1)
    raise Exception("Не удалось подключиться к базе данных")


# Создаем таблицу при первом запуске приложения
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Ошибка инициализации БД: {e}")


@app.get("/")
def read_root():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Фиксируем новое посещение в базе
    cursor.execute("INSERT INTO visits DEFAULT VALUES;")
    conn.commit()

    # Считаем общее количество записей
    cursor.execute("SELECT COUNT(*) FROM visits;")
    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "message": "Привет, БГПУ! Бот и приложение работают в Docker.",
        "total_visits": count
    }