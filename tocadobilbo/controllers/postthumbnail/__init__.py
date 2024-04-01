from typing import Dict

import cloudinary
import cloudinary.uploader
from dynaconf import settings

from tocadobilbo.extensions.database import db
from tocadobilbo.extensions.database.models import Post, PostThumbnail


class CreatePostThumbnailController:
    def post(self, fields: Dict) -> Dict:
        try:
            self.__check_fields(fields)
            self.__create(fields)

        except Exception as error:
            return {'success': False, 'message': str(error)}

        else:
            return {'success': True, 'message': 'Post Thumbnail registered.'}

    def __check_fields(self, fields: Dict) -> None:
        id_post = fields.get('id_post')
        source = fields.get('source')

        if id_post is None:
            raise Exception('Missing required field id_post.')

        elif source is None:
            raise Exception('Missing required field source.')

    def __create(self, fields: Dict) -> None:
        id_post = fields.get('id_post')
        source = fields.get('source')

        if db.session.query(Post).filter(Post.id == id_post).first() is None:
            raise Exception('Post not found.')

        # cloudinary.
        cloud_name = settings.get('CLOUDINARY_NAME')
        api_key = settings.get('CLOUDINARY_KEY')
        api_secret = settings.get('CLOUDINARY_SECRET')

        cloudinary.config(cloud_name=cloud_name, api_key=api_key, api_secret=api_secret)
        upload_result = cloudinary.uploader.upload(source, folder='tocadobilbo-uploads')

        # model.
        secure_url = upload_result.get('secure_url')
        public_id = upload_result.get('public_id')
        postthumbail = PostThumbnail(secure_url=secure_url, public_id=public_id, id_post=id_post)

        db.session.add(postthumbail)
        db.session.commit()


class UpdatePostThumbnailController:
    def post(self, fields: Dict) -> Dict:
        try:
            self.__check_fields(fields)
            self.__update(fields)

        except Exception as error:
            return {'success': False, 'message': str(error)}

        else:
            return {'success': True, 'message': 'Post Thumbnail updated.'}

    def __check_fields(self, fields: Dict) -> None:
        id = fields.get('id')
        id_post = fields.get('id_post')
        source = fields.get('source')

        if id is None:
            raise Exception('Missing required field id.')

        elif id_post is None:
            raise Exception('Missing required field id_post.')

        elif source is None:
            raise Exception('Missing required field source.')

    def __update(self, fields: Dict) -> None:
        id = fields.get('id')
        id_post = fields.get('id_post')
        source = fields.get('source')

        if db.session.query(Post).filter(Post.id == id_post).first() is None:
            raise Exception('Post not found.')

        postthumbail = db.session.query(PostThumbnail).filter(PostThumbnail.id == id).first()

        if postthumbail is None:
            raise Exception('Post Thumbnail not found.')

        # cloudinary.
        cloud_name = settings.get('CLOUDINARY_NAME')
        api_key = settings.get('CLOUDINARY_KEY')
        api_secret = settings.get('CLOUDINARY_SECRET')
        cloudinary.config(cloud_name=cloud_name, api_key=api_key, api_secret=api_secret)
        
        # destroying old image.
        cloudinary.uploader.destroy(postthumbail.public_id)
        
        # uploading new image.
        upload_result = cloudinary.uploader.upload(source, folder='tocadobilbo-uploads')
        secure_url = upload_result.get('secure_url')
        public_id = upload_result.get('public_id')

        # updating.
        postthumbail.public_id = public_id
        postthumbail.secure_url = secure_url
        db.session.commit()


class DeletePostThumbnailController:
    def post(self, fields: Dict) -> Dict:
        try:
            self.__check_fields(fields)
            self.__delete(fields)
        
        except Exception as error:
            return {'success': False, 'message': str(error)}

        else:
            return {'success': True, 'message': 'Post Thumbnail deleted.'}

    def __check_fields(self, fields: Dict) -> None:
        id = fields.get('id')

        if id is None:
            raise Exception('Missing required field id.')

    def __delete(self, fields: Dict) -> None:
        id = fields.get('id')

        postthumbail = db.session.query(PostThumbnail).filter(PostThumbnail.id == id).first()

        if postthumbail is None:
            raise Exception('Post Thumbnail not found.')

        # destroying cloudinary image.
        cloud_name = settings.get('CLOUDINARY_NAME')
        api_key = settings.get('CLOUDINARY_KEY')
        api_secret = settings.get('CLOUDINARY_SECRET')
        cloudinary.config(cloud_name=cloud_name, api_key=api_key, api_secret=api_secret)
        cloudinary.uploader.destroy(postthumbail.public_id)

        # model.
        db.session.delete(postthumbail)
        db.session.commit()
