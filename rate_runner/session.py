"""Manage user authentication with the CREME96 web interface at Vanderbilt """

import logging

import requests
import pytest

from rate_runner import constants

logger = logging.getLogger(__name__)

@pytest.mark.integration
def create_authenticated_session(username: str, password: str) -> requests.Session:
    """Log into CREME96 web interface and return an authenticated session

    Args:
        username (str): CREME96 username
        password (str): CREME96 password

    Returns:
        requests.Session: A session object with login cookies already set

    Raises:
        RuntimeError: If the login request fails or no session cookie is returned

    """
    session = requests.Session()
    login_payload = build_login_payload(username, password)
    response = session.post(constants.CREME96_LOGIN_URL, data=login_payload)
    # Check for non-2xx status
    response.raise_for_status()

    return session

def build_login_payload(username: str, password: str) -> dict[str, str]:
    """Returns a dictionary containing the appropriate CREME96 login fields"""

    # Scraped by looking at the login form submitted in the developer tools
    login_payload = {
        "form.submitted": "1",
        "came_from": f"{constants.CREME96_URL}/CREME-MC",
        "js_enabled": "0",
        "cookies_enabled": "",
        "login_name": "",
        "pwd_empty": "0",
        "__ac_name": username,
        "__ac_password": password,
        "submit": "Log in"
        }
    return login_payload

