from pathlib import Path

from rate_runner.config import get_default_config_path

def test_get_default_config_path_returns_path():
    path = get_default_config_path()
    assert isinstance(path, Path)
    assert path.name == "config.json"
    assert "rate_runner" in str(path)

    
