from ..StorageModels import *

from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field


# user representation to the user/flask
class UserSchema(SQLAlchemySchema):
    class Meta:
        model = UserModel
        load_instance = True

    id          = auto_field()
    username    = auto_field()
    email       = auto_field()
    verified    = auto_field()
    active      = auto_field()
    first_name = auto_field()
    last_name = auto_field()


user_schema = UserSchema( many=True )


