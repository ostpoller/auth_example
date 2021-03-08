import json
import requests

from flask import Blueprint, request, redirect, current_app, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .auth import (
    get_google_client_id,
    get_google_client_secret,
    get_google_client,
    get_google_authorization_endpoint,
    get_google_token_endpoint,
    get_google_userinfo_endpoint
)
from .models import db, User

client = get_google_client()

bp = Blueprint('views', __name__)


@bp.route("/")
def index():
    if current_user.is_authenticated:
        return (
            f"<h2>Hello, {current_user.username}! </h2>"
            f"<p>You're logged in!</p>"
            f"<p>Email: {current_user.email} </p>"
            f"<div><p>Google Profile Picture:</p>"
            f'<img src="{current_user.profile_pic}" alt="Google profile pic"></img></div>'
            f'<a class="button" href="/logout">Logout</a>'
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'


@bp.route("/login")
def login():
    authorization_endpoint = get_google_authorization_endpoint()
    # client = get_google_client()
    current_app.logger.info(f'Google client: {client}')
    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    current_app.logger.info(f'Login request_uri: {request_uri}')
    return redirect(request_uri)


@bp.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    token_endpoint = get_google_token_endpoint()
    # client = get_google_client()
    google_client_id = get_google_client_id()
    google_client_secret = get_google_client_secret()

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(google_client_id, google_client_secret),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = get_google_userinfo_endpoint()
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    # Create a user in your db with the information provided
    # by Google
    user = User(
        id=unique_id, username=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.query.get(unique_id):
        db.session.add(user)
        db.session.commit()

    # Begin user session by logging the user in
    current_app.logger.info(f'Logging in User: {user}')
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("views.index"))


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.index"))
