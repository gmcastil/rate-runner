import os
import sys
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

# Valid configurations need to contain non-empty values for these keys
REQUIRED_CONFIG_KEYS = ["username", "password", "full_name"]

def get_default_config_path() -> Path:
    """Returns default configuration path"""
    system = platform.system()

    if system == "Windows":
        config_home = os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")
    elif system == "Darwin":
        config_home = Path.home() / "Library" / "Application Support"
    else:
        config_home = os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")

    return Path(config_home) / APP_NAME / "config.json"

def load_config_from_file(path: Path = None) -> dict:
    """Load configuration from default location or provided file"""

    # Use a platform dependant default location if none was provided
    if not path:
        path = get_default_config_path()
        logger.debug("No configuration location provided. Using default: {path}")

    if not path.exists():
        logger.error("Configuration not found at: {path}")
        sys.exit(1)

    # Load and validate user configuration
    with open(path, 'r') as f:
        try:
            logger.info("Loading user configuration: {path}")
            user_config = json.load(f)
        except json.JSONDecodeError as err:
            raise ValueError(f"Invalid JSON in configuration: {path}")

    _validate_config(user_config)
    return user_config

def _validate_config(user_config: dict):
    """Raises an exception if user configuration is invalid"""
    for key in REQUIRED_CONFIG_KEYS:
        if not key in user_config:
            raise ValueError(f"Configuration is missing required key: {key}")

