from flask import Blueprint, Flask

from tocadobilbo.blueprints.blog import views


def init_app(app: Flask) -> None:
    blueprint = Blueprint('blog', __name__)
    blueprint.add_url_rule('/', view_func=views.home, endpoint='home')
    blueprint.add_url_rule('/about', view_func=views.about, endpoint='about')
    blueprint.add_url_rule('/albums', view_func=views.albums, endpoint='albums')
    blueprint.add_url_rule('/posts', view_func=views.posts, endpoint='posts')
    blueprint.add_url_rule('/posts/<string:slug>', view_func=views.post_detail, endpoint='post-detail')
    app.register_blueprint(blueprint)
