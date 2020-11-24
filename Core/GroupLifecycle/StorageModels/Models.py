from Core.Shared.DB import db
from sqlalchemy_serializer import SerializerMixin


class GroupMembershipModel( db.Model, SerializerMixin ):
    __tablename__ = 'group_membership'
    __table_args__ = (
        # this can be db.PrimaryKeyConstraint if you want it to be a primary key
        db.UniqueConstraint('group_id', 'assoc_uid'),
    )

    id = db.Column( db.Integer, primary_key=True )

    group_id = db.Column( db.Integer, db.ForeignKey('groups.id' ), nullable=False )
    assoc_uid = db.Column( db.Integer, db.ForeignKey('users.id' ), nullable=False )


class GroupModel( db.Model, SerializerMixin ):
    __tablename__ = 'groups'

    id = db.Column( db.Integer, primary_key=True )
    name = db.Column( db.String(80), unique=True, nullable=False )
    members = db.relationship( "UserModel", secondary='group_membership', cascade="all, delete", back_populates="groups" )


