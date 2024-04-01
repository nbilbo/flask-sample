# https://flask-migrate.readthedocs.io/en/latest/index.html

from flask import Flask
from flask_migrate import Migrate

from tocadobilbo.extensions.database import db
from tocadobilbo.extensions.database.models import User, Post


def init_app(app: Flask) -> None:
    migrate = Migrate()
    migrate.init_app(app, db)
