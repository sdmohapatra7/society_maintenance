import os

class Config:
    # Flask settings
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    DEBUG = True
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", "5000"))

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+pg8000://postgres:password@localhost:5432/society_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email Settings
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "noreply@society.com")

    # Scheduler
    SCHEDULER_API_ENABLED = True
