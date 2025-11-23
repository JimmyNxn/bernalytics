"""
Configuration management for Bernalytics.

This module provides utilities for loading and managing configuration
from environment variables and configuration files.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from loguru import logger
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application configuration loaded from environment variables."""

    # SERP API Configuration
    serp_api_key: str = Field(..., validation_alias="SERP_API_KEY")

    # Search Parameters
    location: str = Field(default="Berlin, Germany", validation_alias="LOCATION")
    job_title: str = Field(default="Data Engineer", validation_alias="JOB_TITLE")
    time_period: str = Field(default="week", validation_alias="TIME_PERIOD")

    # Optional Search Parameters
    employment_type: Optional[str] = Field(default=None, validation_alias="EMPLOYMENT_TYPE")
    experience_level: Optional[str] = Field(default=None, validation_alias="EXPERIENCE_LEVEL")
    remote: Optional[bool] = Field(default=None, validation_alias="REMOTE")

    # Data Storage
    data_dir: Path = Field(default=Path("./data"), validation_alias="DATA_DIR")
    raw_data_dir: Path = Field(default=Path("./data/raw"), validation_alias="RAW_DATA_DIR")
    processed_data_dir: Path = Field(
        default=Path("./data/processed"), validation_alias="PROCESSED_DATA_DIR"
    )

    # Logging Configuration
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    log_file: Optional[Path] = Field(default=None, validation_alias="LOG_FILE")

    # API Rate Limiting
    max_results_per_page: int = Field(default=100, validation_alias="MAX_RESULTS_PER_PAGE")
    max_pages: int = Field(default=10, validation_alias="MAX_PAGES")
    request_delay_seconds: float = Field(default=1.0, validation_alias="REQUEST_DELAY_SECONDS")

    # Database (Optional - for future use)
    database_url: Optional[str] = Field(default=None, validation_alias="DATABASE_URL")

    # Supabase Configuration
    supabase_url: Optional[str] = Field(default=None, validation_alias="SUPABASE_URL")
    supabase_key: Optional[str] = Field(default=None, validation_alias="SUPABASE_KEY")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("time_period")
    @classmethod
    def validate_time_period(cls, v: str) -> str:
        """Validate time period is one of the allowed values."""
        allowed = ["today", "3days", "week", "month"]
        if v.lower() not in allowed:
            raise ValueError(f"time_period must be one of {allowed}, got '{v}'")
        return v.lower()

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is valid."""
        allowed = ["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"log_level must be one of {allowed}, got '{v}'")
        return v.upper()

    @field_validator("data_dir", "raw_data_dir", "processed_data_dir")
    @classmethod
    def ensure_path_exists(cls, v: Path) -> Path:
        """Ensure directory paths exist, create if they don't."""
        if v:
            v.mkdir(parents=True, exist_ok=True)
        return v

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "serp_api_key": "***" if self.serp_api_key else None,  # Mask API key
            "location": self.location,
            "job_title": self.job_title,
            "time_period": self.time_period,
            "employment_type": self.employment_type,
            "experience_level": self.experience_level,
            "remote": self.remote,
            "data_dir": str(self.data_dir),
            "raw_data_dir": str(self.raw_data_dir),
            "processed_data_dir": str(self.processed_data_dir),
            "log_level": self.log_level,
            "log_file": str(self.log_file) if self.log_file else None,
            "max_results_per_page": self.max_results_per_page,
            "max_pages": self.max_pages,
            "request_delay_seconds": self.request_delay_seconds,
            "database_url": "***" if self.database_url else None,  # Mask DB URL
            "supabase_url": "***" if self.supabase_url else None,  # Mask Supabase URL
            "supabase_key": "***" if self.supabase_key else None,  # Mask Supabase key
        }


def load_config(env_file: Optional[str] = None) -> Config:
    """
    Load configuration from environment variables and .env file.

    Args:
        env_file: Path to .env file. If None, will look for .env in current directory.

    Returns:
        Config object with loaded configuration

    Raises:
        ValidationError: If required configuration is missing or invalid
    """
    # Load .env file if it exists
    if env_file:
        load_dotenv(env_file)
    else:
        # Try to find .env in current directory or parent directories
        current_dir = Path.cwd()
        for parent in [current_dir] + list(current_dir.parents):
            env_path = parent / ".env"
            if env_path.exists():
                load_dotenv(env_path)
                logger.info(f"Loaded environment from {env_path}")
                break

    try:
        config = Config()
        logger.info("Configuration loaded successfully")
        logger.debug(f"Configuration: {config.to_dict()}")
        return config
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise


def setup_logging(config: Config) -> None:
    """
    Setup logging configuration.

    Args:
        config: Application configuration
    """
    # Remove default logger
    logger.remove()

    # Add console logger
    logger.add(
        sink=lambda msg: print(msg, end=""),
        level=config.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )

    # Add file logger if configured
    if config.log_file:
        config.log_file.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            sink=config.log_file,
            level=config.log_level,
            rotation="10 MB",
            retention="1 week",
            compression="zip",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        )
        logger.info(f"File logging enabled: {config.log_file}")

    logger.info(f"Logging configured with level: {config.log_level}")


# Global configuration instance (lazy-loaded)
_config: Optional[Config] = None


def get_config(reload: bool = False) -> Config:
    """
    Get the global configuration instance.

    Args:
        reload: If True, reload the configuration from environment

    Returns:
        Config object
    """
    global _config
    if _config is None or reload:
        _config = load_config()
    return _config
