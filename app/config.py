import os
# from pydantic import BaseSettings
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "CRM-POS App"
    APP_VERSION: str = "1.0.0"

    # Database settings
    DATABASE_URL: str = "mysql+pymysql://username:password@localhost:3306/database_name"

    # JWT settings
    JWT_SECRET_KEY: str = "your_secret_key"  # Change this to a secure random value
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # Token expiry time in minutes

    # Payment integration
    JAZZCASH_API_URL: str = "https://sandbox.jazzcash.com.pk"  # Example URL, replace with actual
    JAZZCASH_API_KEY: str = "your_jazzcash_api_key"
    JAZZCASH_SECRET_KEY: str = "your_jazzcash_secret_key"

    class Config:
        env_file = ".env"  # Environment variables can be stored in a .env file

# Create an instance of the settings class
settings = Settings()
