from flask import render_template, request

from tocadobilbo.extensions.database import db
from tocadobilbo.extensions.database.models import Post


def home() -> str:
    return render_template('blog/home.html')


def about() -> str:
    return render_template('blog/about.html')


def albums() -> str:
    return render_template('blog/albums.html')


def posts() -> str:
    posts = db.session.query(Post).order_by(Post.created.desc()).all()
    context = {'posts': posts}

    return render_template('blog/posts.html', **context)


def post_detail(slug: str) -> str:
    post = db.session.query(Post).filter(Post.slug == slug).first()
    context = {'post': post}

    return render_template('blog/post-detail.html', **context)
