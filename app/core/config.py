"""
AGM Store Builder - Core Configuration Settings

This module contains all environment-based settings using Pydantic Settings.
"""

from functools import lru_cache
from typing import List, Optional
from pydantic import field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Uses pydantic-settings for automatic validation and type coercion.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # Application
    NODE_ENV: str = "development"
    PORT: int = 8000
    APP_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:3000"
    APP_NAME: str = "AGM Store Builder"
    APP_VERSION: str = "1.0.0"
    
    @property
    def APP_ENV(self) -> str:
        """Alias for NODE_ENV for backward compatibility."""
        return self.NODE_ENV
    
    @property
    def APP_DEBUG(self) -> bool:
        """Debug mode based on environment."""
        return self.NODE_ENV.lower() != "production"
    
    # Database (MySQL)
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "agm_store_builder"
    DB_SSL: bool = False
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_RECYCLE: int = 3600
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct async MySQL connection URL.
        
        Includes SSL parameters when DB_SSL=true (required for TiDB Cloud).
        """
        base = (
            f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        return base
    
    @property
    def DATABASE_URL_SYNC(self) -> str:
        """Construct sync MySQL connection URL for migrations.
        
        Includes SSL parameters when DB_SSL=true (required for TiDB Cloud).
        """
        base = (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        if self.DB_SSL:
            base += "?ssl_disabled=false"
        return base
    
    # JWT Authentication
    JWT_SECRET: str = "your-super-secret-key-change-in-production"
    JWT_ACCESS_EXPIRY: str = "15m"
    JWT_REFRESH_EXPIRY: str = "7d"
    
    @property
    def JWT_SECRET_KEY(self) -> str:
        """Alias for JWT_SECRET for backward compatibility."""
        return self.JWT_SECRET
    
    @property
    def JWT_ALGORITHM(self) -> str:
        """JWT signing algorithm."""
        return "HS256"
    
    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self) -> int:
        """Parse JWT_ACCESS_EXPIRY to minutes."""
        expiry = self.JWT_ACCESS_EXPIRY
        if expiry.endswith("m"):
            return int(expiry[:-1])
        elif expiry.endswith("h"):
            return int(expiry[:-1]) * 60
        elif expiry.endswith("d"):
            return int(expiry[:-1]) * 60 * 24
        return 15  # Default 15 minutes
    
    @property
    def REFRESH_TOKEN_EXPIRE_DAYS(self) -> int:
        """Parse JWT_REFRESH_EXPIRY to days."""
        expiry = self.JWT_REFRESH_EXPIRY
        if expiry.endswith("d"):
            return int(expiry[:-1])
        elif expiry.endswith("h"):
            return int(expiry[:-1]) // 24
        elif expiry.endswith("m"):
            return int(expiry[:-1]) // (60 * 24)
        return 7  # Default 7 days
    
    # Monnify Payment Gateway
    MONNIFY_BASE_URL: str = "https://sandbox.monnify.com"
    MONNIFY_API_KEY: str = ""
    MONNIFY_SECRET_KEY: str = ""
    MONNIFY_CONTRACT_CODE: str = ""
    MONNIFY_WEBHOOK_SECRET: str = ""
    MONNIFY_REDIRECT_URL: str = ""
    
    @property
    def get_monnify_redirect_url(self) -> str:
        """Get Monnify redirect URL, defaulting to frontend callback."""
        if self.MONNIFY_REDIRECT_URL:
            return self.MONNIFY_REDIRECT_URL
        return f"{self.FRONTEND_URL}/payment/callback"
    
    # Cloudinary (Image Storage)
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    
    # SendGrid (Email)
    SENDGRID_API_KEY: str = ""
    SENDGRID_FROM_EMAIL: str = "noreply@agmshops.com"
    SENDGRID_FROM_NAME: str = "AGM Store Builder"
    
    # Termii (SMS)
    TERMII_API_KEY: str = ""
    TERMII_SENDER_ID: str = "AGMshops"
    TERMII_BASE_URL: str = "https://api.ng.termii.com/api"
    
    # AGM Configuration
    AGM_FEE_PERCENTAGE: float = 2.5
    
    # Rate Limiting
    RATE_LIMIT_WINDOW: int = 15
    RATE_LIMIT_MAX_REQUESTS: int = 100
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # CORS
    CORS_ORIGIN: str = "http://localhost:3000"
    
    @property
    def CORS_ORIGINS(self) -> List[str]:
        """Parse CORS_ORIGIN to list of origins."""
        if "," in self.CORS_ORIGIN:
            return [origin.strip() for origin in self.CORS_ORIGIN.split(",")]
        return [self.CORS_ORIGIN]
    
    # Logging
    LOG_LEVEL: str = "info"
    
    # OTP Configuration
    OTP_EXPIRE_MINUTES: int = 10
    OTP_LENGTH: int = 6
    DEFAULT_OTP: str = "123456"
    USE_DEFAULT_OTP: bool = True
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.NODE_ENV.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.NODE_ENV.lower() == "development"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Uses lru_cache to ensure settings are only loaded once
    and reused throughout the application lifecycle.
    """
    return Settings()


# Export singleton instance for convenience
settings = get_settings()
