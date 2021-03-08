import requests

from flask import current_app
from flask_login import LoginManager
from oauthlib.oauth2 import WebApplicationClient

from .models import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


# OAUTH2 / OPENID SEQUENCE:
# -------------------------
# 1. You register a third-party application as a client to the provider.
# 2. The client sends a request to the provider’s authorization URL.
# 3. The provider asks the user to authenticate (prove who they are).
# 4. The provider asks the user to consent to the client acting on their behalf.
# 5. The provider sends the client a unique authorization code
# 6. The client sends the authorization code back to the provider’s token URL
# 7. The provider sends the client tokens to use with other URLs on behalf of the user


def get_google_client_id():
    return current_app.config["GOOGLE_CLIENT_ID"]


def get_google_client_secret():
    return current_app.config["GOOGLE_CLIENT_SECRET"]


def get_google_provider_cfg():
    google_discovery_url = current_app.config["GOOGLE_DISCOVERY_URL"]
    return requests.get(google_discovery_url).json()


def get_google_client():
    google_client_id = get_google_client_id()
    return WebApplicationClient(google_client_id)


def get_google_authorization_endpoint():
    # Find out what URL to hit for Google login and in response get the authorization code
    google_provider_cfg = get_google_provider_cfg()
    return google_provider_cfg["authorization_endpoint"]


def get_google_token_endpoint():
    # Find out what URL to hit for sending the authorization code back to Google
    # and in response get the token
    google_provider_cfg = get_google_provider_cfg()
    return google_provider_cfg["token_endpoint"]


def get_google_userinfo_endpoint():
    # Find out what URL to hit for requesting userinfo (request must contain the token!)
    google_provider_cfg = get_google_provider_cfg()
    return google_provider_cfg["userinfo_endpoint"]
