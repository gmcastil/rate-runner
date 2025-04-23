import pytest
from pathlib import Path

from rate_runner.config import get_default_config_path
from rate_runner.config import load_config_from_path

def test_get_default_config_path_returns_path():
    path = get_default_config_path()
    assert isinstance(path, Path)
    assert path.name == "config.json"
    assert "rate_runner" in str(path)

def test_load_valid_config():
    config_file = "valid_config.json"
    path = Path(__file__).parent / "config" / config_file
    user_config = load_config_from_path(path)
    assert isinstance(user_config, dict)
    # Check some required keys too
    assert user_config["full_name"] == "Full Name"
    assert user_config["username"] == "my_username"
    assert user_config["password"] == "my_password"

def test_load_config_missing_password_raises():
    invalid_config_file = "invalid_config_missing_password.json"
    path = Path(__file__).parent / "config" / invalid_config_file
    with pytest.raises(KeyError, match="missing required key: password"):
        load_config_from_path(path)

