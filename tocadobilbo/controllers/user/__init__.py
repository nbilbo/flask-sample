from typing import Dict

from tocadobilbo.extensions.database import db
from tocadobilbo.extensions.database.models import User


class CreateUserController:
    def post(self, fields: Dict) -> Dict:
        try:
            self.__check_fields(fields)
            self.__create(fields)

        except Exception as error:
            return {'success': False, 'message': str(error)}

        else:
            return {'success': True, 'message': 'User created.'}
        

    def __check_fields(self, fields: Dict) -> None:
        username = fields.get('username')
        password = fields.get('password')

        if username is None:
            raise Exception('Missing required field username.')

        elif password is None:
            raise Exception('Missing required field password.')

    def __create(self, fields: Dict) -> None:
        username = fields.get('username')
        password = fields.get('password')
        register = db.session.query(User).filter(User.username == username).first()

        if register is not None:
            raise Exception('Username already registered.')

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()


class UpdateUserController:
    def post(self, fields: Dict) -> Dict:
        try:
            self.__check_fields(fields)
            self.__update(fields)

        except Exception as error:
            return {'success': False, 'message': str(error)}

        else:
            return {'success': True, 'message': 'User updated.'}
    
    def __check_fields(self, fields: Dict) -> None:
        id = fields.get('id')
        username = fields.get('username')
        password = fields.get('password')

        if id is None:
            raise Exception('Missing required field id.')

        if username is None:
            raise Exception('Missing required field username.')

        if password is None:
            raise Exception('Missing required field password.')

    def __update(self, fields: Dict) -> None:
        id = fields.get('id')
        username = fields.get('username')
        password = fields.get('password')

        if db.session.query(User).filter(User.id != id, User.username == username).first() is not None:
            raise Exception('Username already registered.')

        user = db.session.query(User).filter(User.id == id).first()

        if user is None:
            raise Exception('User not found.')

        user.username = username
        user.password = password
        db.session.commit()
