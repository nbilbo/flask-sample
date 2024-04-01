from datetime import datetime
from typing import Any, List

import bleach
from markdown import markdown
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tocadobilbo.extensions.database import db


class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created: Mapped[datetime] = mapped_column(default=datetime.now)
    posts: Mapped[List['Post']] = relationship(back_populates='user')

    def __str__(self) -> str:
        return str(self.username)


class Post(db.Model):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(nullable=False, unique=True)
    body: Mapped[str] = mapped_column(nullable=False)
    body_html: Mapped[str] = mapped_column(nullable=False)
    created: Mapped[datetime] = mapped_column(default=datetime.now)

    id_user: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='posts')

    thumbnail: Mapped['PostThumbnail'] = relationship(back_populates='post')

    def __str__(self) -> str:
        return str(self.title)


class PostThumbnail(db.Model):
    __tablename__ = 'post_thumbnail'

    id: Mapped[int] = mapped_column(primary_key=True)
    secure_url: Mapped[str] = mapped_column(nullable=False)
    public_id: Mapped[int] = mapped_column(nullable=False)

    id_post: Mapped[int] = mapped_column(ForeignKey('post.id'), unique=True)
    post: Mapped['Post'] = relationship(back_populates='thumbnail', uselist=False)


def on_changed_body(target: 'Post', value: str, oldvalue: Any, initiator: Any) -> None:
    # https://www.gitauharrison.com/articles/rich-text

    allowed_tags = [
        'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1',
        'h2', 'h3', 'p'
    ]

    target.body_html = bleach.linkify(
        bleach.clean(markdown(value, output_format='html'),
        tags=allowed_tags, strip=True)
    )


db.event.listen(Post.body, 'set', on_changed_body)
