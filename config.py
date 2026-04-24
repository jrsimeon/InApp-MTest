from pydantic_settings import BaseSettings
from pydantic import Field, EmailStr


class Settings(BaseSettings):
    # 🔐 App
    APP_NAME: str = "Flask Auth App"
    DEBUG: bool = True

    # 🔐 JWT
    JWT_SECRET_KEY: str = Field(..., min_length=10)
    JWT_ACCESS_TOKEN_EXPIRES: int = Field(3600, ge=60, le=86400)  # 1 min to 24 hrs

    # 🗄️ Database
    DATABASE_URL: str = "sqlite:///database/MovieInfo.db"

    # 📧 Example validation
    ADMIN_EMAIL: EmailStr

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    SQLITE_DB_NAME: str

    class Config:
        env_file = ".env"
        case_sensitive = True


# Singleton instance
settings = Settings()