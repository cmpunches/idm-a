from ..StorageModels import *

from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from enum import Enum, auto
import json


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


user_schema = UserSchema(many=True)


class STATUS(Enum):
    SUCCESS         = auto()
    DATA_CONFLICT   = auto()
    DATA_STRUCTURE  = auto()
    FAILURE         = auto()


class EResp:
    def __init__( self, status, message, attachment=None ):
        self.status = status
        self.message = message

        if attachment is not None:
            self.attachment = attachment
        else:
            self.attachment = "NULL"

    def to_json(self):
        serialized_self = dict()
        serialized_self['status'] = self.status.name
        serialized_self['message'] = self.message
        if self.attachment != "NULL":
            serialized_self['attachment'] = json.loads( self.attachment )
        serialized_self['attachment'] = None

        return serialized_self

    def __repr__(self):
        return self.to_json()

    def __str__(self):
        return self.to_json()