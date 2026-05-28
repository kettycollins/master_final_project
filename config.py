import os


class Config:
    """Централізовані налаштування безпеки та конфігурації додатку."""

    # Секретний ключ для підпису сесій Flask
    # У реальних системах береться з екологічних змінних (Environment Variables)
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "supersecret_zero_trust_key_2026")

    # Шлях до бази даних SQLite
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_PATH = os.path.join(BASE_DIR, "data", "users.db")

    # Налаштування логів
    LOG_FILE = os.path.join(BASE_DIR, "logs", "access_logs.json")
