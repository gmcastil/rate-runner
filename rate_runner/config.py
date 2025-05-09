import os
import platform
import logging
import json
from pathlib import Path

from rate_runner import constants

logger = logging.getLogger(__name__)

# Valid configurations need to contain non-empty values for these keys
REQUIRED_CONFIG_KEYS = ("username", "password", "full_name")

def get_default_config_path() -> Path:
    """Returns default configuration path"""
    system = platform.system()

    if system == "Windows":
        config_home = os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")
    elif system == "Darwin":
        config_home = Path.home() / "Library" / "Application Support"
    else:
        config_home = os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")

    return Path(config_home) / constants.APP_NAME / "config.json"

def load_config_from_path(path: Path = None) -> dict:
    """Load configuration from default location or provided path"""

    # Use a platform dependant default location if none was provided
    if not path:
        path = get_default_config_path()
        logger.debug("No configuration location provided. Using default: %s", path)

    if not path.exists():
        logger.error("Configuration file not found at: %s", path)
        raise FileNotFoundError(f"Configuration file not found at: {path}")

    # Load and validate user configuration
    with open(path, 'r') as f:
        try:
            logger.info("Loading user configuration: %s", path)
            user_config = json.load(f)
        except json.JSONDecodeError:
            logger.error("Invalid JSON in configuration: %s", path)
            raise ValueError(f"Invalid JSON in configuration: {path}")

    _validate_config(user_config)
    return user_config

def _validate_config(user_config: dict):
    """Raises an exception if user configuration is invalid"""
    for key in REQUIRED_CONFIG_KEYS:
        if key not in user_config:
            raise KeyError(f"Configuration missing required key: {key}")

