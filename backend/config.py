# RESETA™ Enterprise Backend Configuration
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "RESETA™ Enterprise"
    DEVELOPER_ENTITY: str = "Qsura India Pvt. Ltd."
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./reseta.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "reseta-enterprise-super-secure-secret-token-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours
    MIN_COHORT_SIZE: int = 5 # Minimum cohort threshold for privacy aggregation
    TELE_MANAS_HELPLINE: str = "14416 / 1800-89-14416"
    DEFAULT_TENANT_ID: str = "org-technova-01"

    model_config = {"case_sensitive": True}


settings = Settings()
