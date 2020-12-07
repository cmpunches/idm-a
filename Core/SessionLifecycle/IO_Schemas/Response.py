from marshmallow_sqlalchemy import auto_field, SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from Core.UserLifecycle.IO_Schemas import *
from Core.SessionLifecycle.StorageModels import *


class Session(SQLAlchemyAutoSchema):
    class Meta:
        model = SessionModel
        include_relationships = True
        load_instance = True

    token            = auto_field()
    timestamp        = auto_field()

    uid              = auto_field()


session_schema = Session( many=True )
