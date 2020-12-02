from ..StorageModels import *
from Core.UserLifecycle.IO_Schemas.Response import *
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested


class Session(SQLAlchemyAutoSchema):
    class Meta:
        model = SessionModel
        include_relationships = True
        load_instance = True

    token            = auto_field()
    timestamp        = auto_field()

    uid              = auto_field()
    assoc_user       = Nested( UserSchema, many=True, exclude=["sessions"])

session_schema = Session( many=True )
