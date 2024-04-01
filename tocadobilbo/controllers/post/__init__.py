from typing import Dict

from tocadobilbo.extensions.database import db
from tocadobilbo.extensions.database.models import Post, User


class CreatePostController:
    def post(self, fields: Dict) -> Dict:
        try:
            self.__check_fields(fields)
            self.__create(fields)

        except Exception as error:
            return {'success': False, 'message': str(error)}

        else:
            return {'success': True, 'message': 'Post created.'}

    def __check_fields(self, fields: Dict) -> None:
        id_user = fields.get('id_user')
        title = fields.get('title')
        slug = fields.get('slug')
        body = fields.get('body')

        if id_user is None:
            raise Exception('Missing required field id_user.')

        elif title is None:
            raise Exception('Missing required field title.')

        elif slug is None:
            raise Exception('Missing required field slug.')

        elif body is None:
            raise Exception('Missing required field body.')

    def __create(self, fields: Dict) -> None:
        id_user = fields.get('id_user')
        title = fields.get('title')
        slug = fields.get('slug')
        body = fields.get('body')

        if db.session.query(Post).filter(Post.title == title).first():
            raise Exception('Title already registered.')

        if db.session.query(Post).filter(Post.slug == slug).first():
            raise Exception(' Slug already registered.')

        if db.session.query(User).filter(User.id == id_user).first() is None:
            raise Exception(' User not found.')

        post = Post(title=title, slug=slug, body=body, id_user=id_user)
        db.session.add(post)
        db.session.commit()


class UpdatePostController:
    def post(self, fields: Dict) -> Dict:
        try:
            self.__check_fields(fields)
            self.__update(fields)

        except Exception as error:
            return {'success': False, 'message': str(error)}

        else:
            return {'success': True, 'message': 'Post updated.'}

    def __check_fields(self, fields: Dict) -> None:
        id = fields.get('id')
        id_user = fields.get('id_user')
        title = fields.get('title')
        slug = fields.get('slug')
        body = fields.get('body')

        if id is None:
            raise Exception('Missing required field id.')

        if id_user is None:
            raise Exception('Missing required field id_user.')

        if title is None:
            raise Exception('Missing required field title.')

        if slug is None:
            raise Exception('Missing required field slug.')

        if body is None:
            raise Exception('Missing required field body.')

    def __update(self, fields: Dict) -> None:
        id = fields.get('id')
        id_user = fields.get('id_user')
        title = fields.get('title')
        slug = fields.get('slug')
        body = fields.get('body')

        if db.session.query(Post).filter(Post.id != id, Post.title == title).first():
            raise Exception('Title already registered.')

        if db.session.query(Post).filter(Post.id != id, Post.slug == slug).first():
            raise Exception('Slug already registered.')

        if db.session.query(User).filter(User.id == id_user).first() is None:
            raise Exception('User not found.')

        post = db.session.query(Post).filter(Post.id == id).first()

        if post is None:
            raise Exception('Post not found.')

        post.id_user = id_user
        post.title = title
        post.slug = slug
        post.body = body
        db.session.commit()
