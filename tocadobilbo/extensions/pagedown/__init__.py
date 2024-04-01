from flask import Flask
from flask_pagedown import PageDown


def init_app(app: Flask) -> None:
    pagedown = PageDown()
    pagedown.init_app(app)
