# RESETA™ Enterprise Backend Configuration
import os
from pydantic_settings import BaseSettings
from pydantic import model_validator

class Settings(BaseSettings):
    APP_NAME: str = "RESETA™ Enterprise"
    DEVELOPER_ENTITY: str = "Qsura India Pvt. Ltd."
    PROPRIETARY_ENTITY: str = "Qsura India Pvt. Ltd."
    FOUNDER_AND_ARCHITECT: str = "Dr. Irfan Ashraf"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./reseta.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "reseta-enterprise-super-secure-secret-token-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours
    MIN_COHORT_SIZE: int = 5 # Minimum cohort threshold for privacy aggregation
    TELE_MANAS_HELPLINE: str = "14416 / 1800-89-14416"
    DEFAULT_TENANT_ID: str = "org-technova-01"
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000,http://localhost:3000,https://reseta.enterprise")

    model_config = {"case_sensitive": True}

    @model_validator(mode="after")
    def validate_production_secrets(self):
        if self.ENVIRONMENT.lower() == "production":
            if self.SECRET_KEY == "reseta-enterprise-super-secure-secret-token-2026" or len(self.SECRET_KEY) < 32:
                raise ValueError(
                    "FATAL SECURITY MISCONFIGURATION: In production mode, SECRET_KEY must be an externally supplied, "
                    "high-entropy secret string with at least 32 characters. Default development signing keys are strictly blocked."
                )
        return self

settings = Settings()
