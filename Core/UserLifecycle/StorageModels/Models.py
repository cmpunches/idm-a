from Core.Shared.DB import db
from datetime import datetime
import uuid
from sqlalchemy_serializer import SerializerMixin

from Core.GroupLifecycle.StorageModels.Models import GroupMembershipModel
from Core.SessionLifecycle.StorageModels.Models import SessionModel


def gen_uuid4():
    return str( uuid.uuid4() )


# user representation to the ORM
class UserModel( db.Model, SerializerMixin ):
    __tablename__ = 'users'
    # Creation of a user is not dependent on any external record.
    # Deletion of a user should delete its associated sessions and any group association records

    id          = db.Column( db.Integer,        primary_key=True                        )
    username    = db.Column( db.String(80),     unique=True,        nullable=False      )
    email       = db.Column( db.String(120),    unique=True,        nullable=False      )
    verified    = db.Column( db.Boolean,                            default=False       )
    password    = db.Column( db.String(50),                         nullable=False      )
    first_name  = db.Column( db.String(50),                         nullable=False      )
    last_name   = db.Column( db.String(50),                         nullable=False      )
    active      = db.Column( db.Boolean,                            default=True        )

    # many-to-many
    groups = db.relationship( 'GroupModel', secondary='group_membership', cascade="all, delete" )

    # one-to-many
    sessions = db.relationship( 'SessionModel', cascade="all, delete" )


class EmailValidationModel( db.Model, SerializerMixin ):
    __tablename__ = 'email_validation'
    # each entry gets an index
    # a timestamp so we can expire them as they get old
    # tie the email it's associated with to an actual user's email to prevent $CRIME
    # the validation code they need to verify their email
    id          = db.Column( db.Integer,  primary_key=True )
    timestamp   = db.Column( db.DateTime, default=datetime.now )

    # one-to-one
    email       = db.Column( db.String(120), db.ForeignKey('users.email' ), nullable=False, unique=True )
    code        = db.Column( db.String(36), unique=True, default=gen_uuid4 )

