import os
import pytest

from rate_runner.session import create_authenticated_session
from rate_runner.session import build_login_payload

def test_login_payload_format():
    payload = build_login_payload("myuser", "mypassword")

    assert isinstance(payload, dict)
    assert "__ac_name" in payload
    assert "__ac_password" in payload
    assert payload["__ac_name"] == "myuser"
    assert payload["__ac_password"] == "mypassword"
    assert all(isinstance(v, str) for v in payload.values())

