from Core.Shared.DB import db
import uuid
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin


def generate_token():
    # UUID4 for now -- must change this to something else at some point to prevent CRIME
    return str( uuid.uuid4() )


class SessionModel( db.Model, SerializerMixin ):
    __tablename__ = 'sessions'

    # tokens can have only one user
    # token should be a UUID
    token = db.Column( db.String(36), primary_key=True, default=generate_token, unique=True )

    # the associated user
    # users can have more than one token
    # many-to-one
    uid = db.Column( db.Integer, db.ForeignKey( 'users.id' ), nullable=False, unique=False )

    # the associated user
    # user object to serve as bridge to group membership and other user details
    # many-to-one
    assoc_user = db.relationship( 'UserModel', cascade="all, delete", back_populates="sessions" )

    # the creation time of the session
    timestamp = db.Column( db.DateTime, default=datetime.now, nullable=False )