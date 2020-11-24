from Core.GroupLifecycle.StorageModels.Models import *

from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field


# group representation to the user/flask
class GroupSchema(SQLAlchemySchema):
    class Meta:
        model = GroupModel
        load_instance = True

    id      = auto_field()
    name    = auto_field()


group_schema = GroupSchema( many=True )
