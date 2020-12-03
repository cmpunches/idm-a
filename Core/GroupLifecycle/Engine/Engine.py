from Core.GroupLifecycle.IO_Schemas import *
from Core.UserLifecycle.IO_Schemas import *
from Core.Shared.ResponseSchema import *

from sqlalchemy import exc


class GroupLifeCycleController:
    def __init__(self, context_sensitive=True):
        # False is root
        self.session_aware = context_sensitive

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
                return EResp( STATUS.NOT_FOUND, "Either that user or that group does not exist!", resp_attache )

        return EResp( STATUS.SUCCESS, "User added to group.", resp_attache )

    def remove_user_from_group(self, user_id, group_id):
        group_association = GroupMembershipModel.query.filter_by( assoc_uid=user_id, group_id=group_id ).first()
        if group_association is not None:
            resp_attache = json.dumps( group_association.to_dict(), indent=4, sort_keys=True )
            db.session.delete( group_association )
            db.session.commit()

            return EResp( STATUS.SUCCESS, "UID '{0}' removed from GID '{1}'".format( user_id, group_id ), None )
        else:
            return EResp( STATUS.NOT_FOUND, "UID '{0}' is not in GID '{1}'!".format( user_id, group_id ), None )

    def get_associated_groups(self, user_id ):
        user = UserModel.query.get( user_id )

        if user is not None:
            resp_attach = group_schema.dumps( user.groups )
            return EResp( STATUS.SUCCESS, "Groups found for user.", resp_attach )
        else:
            return EResp( STATUS.NOT_FOUND, "User ID is not found.", None )

    def delete_group( self, id ):
        group = GroupModel.query.filter_by( id=id ).first()

        if group is not None:
            resp_attache = group_schema.dumps( [ group ] )

            group.members = []
            db.session.delete( group )
            # need a try/catch block here
            db.session.commit()

            return EResp( STATUS.SUCCESS, "Group deleted.", resp_attache )
        else:
            return EResp( STATUS.NOT_FOUND, "This group does not exist.", None )

    def get_group_members(self, id ):
        group = GroupModel.query.filter_by( id=id ).first()

        if group is not None:
            members = group.members
            resp_attache = user_schema.dumps( members )
            return EResp( STATUS.SUCCESS, "Group members found.", resp_attache )
        else:
            return EResp( STATUS.NOT_FOUND, "No group found.", None )

    def update_group_details(self, gid, group_name ):
        group = GroupModel.query.get( gid )

        resp_attache = group_schema.dumps( [ group ] )
        if group is not None:
            if group.name != group_name:
                group.name = group_name
                # need a try/catch block here
                db.session.commit()
        else:
            return EResp( STATUS.NOT_FOUND, "Group not found!", None )

        return EResp( STATUS.SUCCESS, "Group updated.", group )

    # is the provided session associated with a user in group X?
    def group_in_context( self, context, group ):
        user = context.assoc_user
        membership = user.groups

        if group in membership:
            return True
        else:
            return False

    def group_exists(self, group_name, context=None ):
        group = GroupModel.query.filter_by( name=group_name ).first()

        if group is not None:
            return True
        else:
            return False
