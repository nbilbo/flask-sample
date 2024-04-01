# https://www.dynaconf.com/flask/

from dynaconf import FlaskDynaconf
from flask import Flask


def init_app(app: Flask) -> None:
    flask_dynaconf = FlaskDynaconf(extensions_list='EXTENSIONS')
    flask_dynaconf.init_app(app)
