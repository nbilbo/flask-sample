# https://flask-admin.readthedocs.io/en/latest/introduction/#getting-started

from flask import Flask
from flask_admin import Admin

from tocadobilbo.extensions.admin import views
from tocadobilbo.extensions.database import db
from tocadobilbo.extensions.database.models import User, Post, PostThumbnail


def init_app(app: Flask) -> None:
    admin = Admin(name='tocadobilbo', template_mode='bootstrap3')
    admin.add_view(views.UserModelView(User, db.session, name='Users'))
    admin.add_view(views.PostModelView(Post, db.session, name='Posts'))
    admin.add_view(views.PostThumbnailModelView(PostThumbnail, db.session, name='Post Thumbnail'))
    admin.init_app(app)
