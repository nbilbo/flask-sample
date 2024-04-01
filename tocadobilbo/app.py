# https://flask.palletsprojects.com/en/2.2.x/api/?highlight=flask#flask.Flask

from flask import Flask

from tocadobilbo.extensions import configurations


def create_app():
    app = Flask(__name__.split('.')[0], static_folder='../static', template_folder='../templates')
    configurations.init_app(app)

    return app
