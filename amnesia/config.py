"""Default configuration

Use env var to override
"""
from datetime import timedelta

DEBUG = True
SECRET_KEY = "changeme"

SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/amnesia.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=365)
