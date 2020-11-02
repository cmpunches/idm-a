from Core.Shared.DB import db


# user representation to the ORM
class UserModel(db.Model):
    id          = db.Column( db.Integer,        primary_key=True                        )
    username    = db.Column( db.String(80),     unique=True,        nullable=False      )
    email       = db.Column( db.String(120),    unique=True,        nullable=False      )
    verified    = db.Column( db.Boolean,                            default=False       )
    password    = db.Column( db.String(50),                         nullable=False      )
    active      = db.Column( db.Boolean,                            default=True        )

    def __repr__(self):
        return '<User %r>' % self.username


