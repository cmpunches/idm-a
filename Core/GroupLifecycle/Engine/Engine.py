from Core.GroupLifecycle.StorageModels import *
from Core.GroupLifecycle.IO_Schemas import *
from config import *
from Core.Shared.ResponseSchema import *

from sqlalchemy import exc


class GroupLifeCycleController:
    def __init__(self):
        pass

    def get_all_groups(self):
        groups = GroupModel.query.all()
        return EResp( STATUS.SUCCESS, "Dumping ALL groups.", group_schema.dumps( groups ) )

    def create_group(self, name ):
        group = GroupModel( name=name )

        db.session.add(group)

        resp_attache = group_schema.dumps( [ group ] )

        try:
            db.session.commit()
        except exc.IntegrityError as err:
            if err.orig.args[0] == 1062:
                db.session.rollback()
                return EResp( STATUS.DATA_CONFLICT, "Group already exists.", resp_attache )

        return EResp( STATUS.SUCCESS, "Group successfully created.", resp_attache )

    def add_user_to_group(self, user_id, group_id ):
        # adds an existing user to an existing group
        group_association = GroupMembershipModel( group_id=group_id, assoc_uid=user_id )

        db.session.add( group_association )

        resp_attache = json.dumps( group_association.to_dict(), indent=4, sort_keys=True )

        try:
            db.session.commit()
        except exc.IntegrityError as err:
            db.session.rollback()
            if err.orig.args[0] == 1062:
                return EResp( STATUS.DATA_CONFLICT, "User is already in this group.", resp_attache )
            if err.orig.args[0] == 1452:
                return EResp( STATUS.DATA_STRUCTURE, "Either that user or that group does not exist!", resp_attache )

        return EResp( STATUS.SUCCESS, "User added to group.", resp_attache )

    def remove_user_from_group(self, user_id, group_id):
        group_association = GroupMembershipModel.query.filter_by( assoc_uid=user_id, group_id=group_id ).first()
        if group_association is not None:
            resp_attache = json.dumps( group_association.to_dict(), indent=4, sort_keys=True )
            db.session.delete( group_association )
            db.session.commit()

            return EResp( STATUS.SUCCESS, "UID '{0}' removed from GID '{1}'".format( user_id, group_id ), None )
        else:
            return EResp( STATUS.DATA_CONFLICT, "UID '{0}' is not in GID '{1}'!".format( user_id, group_id ), None )

    def delete_group( self, id ):
        group = GroupModel.query.filter_by( id=id ).first()

        if group is not None:
            resp_attache = group_schema.dumps( [ group ] )

            group.members = []
            db.session.delete( group )
            db.session.commit()

            return EResp( STATUS.SUCCESS, "Group deleted.", resp_attache )
        else:
            return EResp( STATUS.DATA_CONFLICT, "This group does not exist.", None )