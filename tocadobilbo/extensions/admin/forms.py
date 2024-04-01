# https://wtforms-sqlalchemy.readthedocs.io/en/latest/wtforms_sqlalchemy/

from typing import List

from flask_admin.model.form import InlineFormAdmin
from flask_pagedown.fields import PageDownField
from wtforms import FileField, PasswordField, StringField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms_sqlalchemy.orm import Form

from tocadobilbo.extensions.database import db
from tocadobilbo.extensions.database.models import User, Post


def enabled_users() -> List[User]:
    return db.session.query(User).all()


def enabled_posts() -> List[Post]:
    return db.session.query(Post).all()


class InlinePostThumbnailForm(InlineFormAdmin):
    # source = StringField('Source', validators=[DataRequired()])
    form_columns = ('source', )


class UserForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class PostForm(Form):
    user = QuerySelectField(query_factory=enabled_users, allow_blank=False)
    title = StringField('Title', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    body = PageDownField('Body', validators=[DataRequired()])


class PostThumbnailForm(Form):
    post = QuerySelectField(query_factory=enabled_posts, allow_blank=False)
    source = FileField('Source', validators=[DataRequired()])
