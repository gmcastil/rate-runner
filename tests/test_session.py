import pytest

from rate_runner import constants
from rate_runner.session import create_authenticated_session
from rate_runner.session import build_login_payload
from rate_runner.config import get_default_config_path
from rate_runner.config import load_config_from_path

def test_login_payload_format():
    payload = build_login_payload("myuser", "mypassword")

    assert isinstance(payload, dict)
    assert "__ac_name" in payload
    assert "__ac_password" in payload
    assert payload["__ac_name"] == "myuser"
    assert payload["__ac_password"] == "mypassword"
    assert all(isinstance(v, str) for v in payload.values())

@pytest.mark.integration
def test_create_login_session():

    path = get_default_config_path()

    # Users need to create their own configuration to run integration tests
    if not path.exists():
        pytest.skip(f"Configuraton file not found at {path} - skipping integration test")

    try:
        user_config = load_config_from_path()
    except Exception as err:
        pytest.fail(f"Failed to load configuration: {err}")

    username = user_config["username"]
    password = user_config["password"]
    session = create_authenticated_session(username, password)
    # URL that should only be accessible if login was successful
    protected_url = f"{constants.CREME96_URL}/CREME-MC/Members/{username}"
    response = session.get(protected_url)
    response.raise_for_status()

    # Use the presence of the 'Log out' option to determine if we were successful
    assert "Log out" in response.text
    # Full name is something that has to be supplied in the configuration, so it can be a
    # reliable indicator of whether log in was successful
    assert user_config["full_name"] in response.text

