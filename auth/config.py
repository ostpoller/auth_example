import os

projectdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    DATA_DIR = os.environ.get("DATA_DIR") or os.path.join(projectdir, 'data')
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        'sqlite:///' + os.path.join(DATA_DIR, 'auth.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"


class TestingConfig(Config):
    pass
