from Core.GroupLifecycle.IO_Schemas import *
from Core.UserLifecycle.IO_Schemas import *
from Core.Shared.ResponseSchema import *
from Core.SessionLifecycle.Engine import *
from sqlalchemy import exc
from Core.Shared.Decorators import *

# GROUP ENGINE


class GroupLifeCycleController:
    def __init__(self, context_sensitive=True):
        # False is root
        self.session_aware = context_sensitive

#    @require_active_session
    @require_access_level( group=idma_conf.administration['admin_group'] )
    def get_all_groups( self, context=None ):
        groups = GroupModel.query.all()
        return EResp( STATUS.SUCCESS, "Dumping ALL groups.", group_schema.dumps( groups ) )

    @require_access_level( group=idma_conf.administration['admin_group'] )
    def create_group(self, name, context=None ):
        group = GroupModel( name=name )

        db.session.add(group)

        try:
            db.session.commit()
        except exc.IntegrityError as err:
            if err.orig.args[0] == 1062:
                db.session.rollback()
                return EResp( STATUS.DATA_CONFLICT, "Group already exists.", group_schema.dumps( [ group ] ) )

        return EResp( STATUS.SUCCESS, "Group successfully created.", group_schema.dumps( [ group ] ) )

    @require_access_level( group=idma_conf.administration['admin_group'] )
    def add_user_to_group(self, user_id, group_id, context=None ):
        # adds an existing user to an existing group
        group_association = GroupMembershipModel( group_id=group_id, assoc_uid=user_id )

        db.session.add( group_association )

        try:
            db.session.commit()
        except exc.IntegrityError as err:
            db.session.rollback()
            if err.orig.args[0] == 1062:
                return EResp( STATUS.DATA_CONFLICT, "User is already in this group.", None )
            if err.orig.args[0] == 1452:
                return EResp( STATUS.NOT_FOUND, "Either that user or that group does not exist!", json.dumps( group_association.to_dict(), indent=4, sort_keys=True ) )

        return EResp( STATUS.SUCCESS, "User added to group.", json.dumps( group_association.to_dict(), indent=4, sort_keys=True ) )

    @require_access_level( group=idma_conf.administration['admin_group'] )
    def remove_user_from_group( self, user_id, group_id, context=None ):
        group_association = GroupMembershipModel.query.filter_by( assoc_uid=user_id, group_id=group_id ).first()
        if group_association is not None:
            resp_attache = json.dumps( group_association.to_dict(), indent=4, sort_keys=True )
            db.session.delete( group_association )
            db.session.commit()

            return EResp( STATUS.SUCCESS, "UID '{0}' removed from GID '{1}'".format( user_id, group_id ), None )
        else:
            return EResp( STATUS.NOT_FOUND, "UID '{0}' is not in GID '{1}'!".format( user_id, group_id ), None )

    @require_access_level( group=idma_conf.administration['admin_group'] )
    def get_associated_groups(self, user_id, context=None ):
        user = UserModel.query.get( user_id )

        if user is not None:
            resp_attach = group_schema.dumps( user.groups )
            return EResp( STATUS.SUCCESS, "Groups found for user.", resp_attach )
        else:
            return EResp( STATUS.NOT_FOUND, "User ID is not found.", None )

    @require_access_level( group=idma_conf.administration['admin_group'] )
    def delete_group( self, id, context=None ):
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

    @require_access_level( group=idma_conf.administration['admin_group'] )
    def get_group_members( self, id, context=None ):
        group = GroupModel.query.filter_by( id=id ).first()

        if group is not None:
            members = group.members
            resp_attache = user_schema.dumps( members )
            return EResp( STATUS.SUCCESS, "Group members found.", resp_attache )
        else:
            return EResp( STATUS.NOT_FOUND, "No group found.", None )

    @require_access_level( group=idma_conf.administration['admin_group'] )
    def update_group_details( self, gid, group_name, context=None ):
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

    def get_group_by_name( self, group_name ):
        group = GroupModel.query.filter_by( name=group_name ).first()

        if group is not None:
            return EResp( STATUS.SUCCESS, "Sending group details.", group_schema.dumps( [ group ] ))
        else:
            return EResp( STATUS.NOT_FOUND, "Group does not exist.", None )
