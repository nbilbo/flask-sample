# https://pypi.org/project/Flask-SQLAlchemy/

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def init_app(app: Flask) -> None:
    db.init_app(app)
