from Core.Shared.DB import db
from datetime import datetime
import uuid


def gen_uuid4():
    return str(uuid.uuid4())

# user representation to the ORM
class UserModel(db.Model):
    __tablename__ = 'users'

    id          = db.Column( db.Integer,        primary_key=True                        )
    username    = db.Column( db.String(80),     unique=True,        nullable=False      )
    email       = db.Column( db.String(120),    unique=True,        nullable=False      )
    verified    = db.Column( db.Boolean,                            default=False       )
    password    = db.Column( db.String(50),                         nullable=False      )
    active      = db.Column( db.Boolean,                            default=False       )

    def __repr__(self):
        return '<User %r>' % self.username


class EmailValidation(db.Model):
    __tablename__ = 'email_validation'
    # each entry gets an index
    # a timestamp so we can expire them as they get old
    # tie the email it's associated with to an actual user's email to prevent $CRIME
    # the validation code they need to verify their email
    id          = db.Column( db.Integer,  primary_key=True )
    timestamp   = db.Column( db.DateTime, default=datetime.now() )
    email       = db.Column( db.String(120), db.ForeignKey('users.email'), nullable=False, unique=True )
    code        = db.Column( db.String(36), unique=True, default=gen_uuid4 )

    def __repr__(self):
        return '<EmailValidation %r>' % self.email
