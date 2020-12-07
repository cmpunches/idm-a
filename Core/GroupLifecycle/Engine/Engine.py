from Core.GroupLifecycle.IO_Schemas import *
from Core.UserLifecycle.IO_Schemas import *
from Core.Shared.ResponseSchema import *
from Core.SessionLifecycle.Engine import *
from sqlalchemy import exc
from functools import wraps

# GROUP ENGINE

# Decorator to require just an active session.  This allows you to create public/private.
def require_active_session(method):
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):
        if self.session_aware:
            print("DBUG: The Auth layer is enabled.")
            if 'context' in method_kwargs.keys():
                print("DBUG: Context was provided to the call. ('{0}')".format(method_kwargs['context']))
                if not self.session_controller.session_is_active(token=method_kwargs['context']):
                    print("DBUG: The context is an inactive or non-existent session.")
                    return EResp(STATUS.NOT_AUTHORIZED, "This action requires an active session.", None)
                else:
                    print("DBUG: The context is an active session.")
                    return method(self, *method_args, **method_kwargs)
            else:
                print("DBUG: Auth layer is enabled but no context provided.")
                return EResp(STATUS.NOT_AUTHORIZED, "This action requires an active session.", None)
        else:
            print("DBUG The auth layer is not enabled.  Disregarding context.")
            return method(self, *method_args, **method_kwargs)
        return EResp( STATUS.NOT_AUTHORIZED, "This action requires an active session.", None )
    return _impl

# Decorate to require a specific group membership.  This allows granular access control.
def require_access_level( group ):
    def require_privilege(f):
        @wraps(f)
        def _impl(self, *method_args, **method_kwargs):
            if self.session_aware:
                print("DBUG: Auth layer is enabled.")

                print("DBUG: This method requires a context from a user in group '{0}'.".format( group ) )
                print("DBUG: Context was provided to the call. ('{0}')".format(method_kwargs['context']))
                session = self.session_controller.get_session_object( method_kwargs['context'] )
                user = session.assoc_user
                print("DBUG: Associated user with this session is '{0}'.".format(user.username))
                groups = [usergroup.name for usergroup in session.assoc_user.groups]
                print("DBUG: This user in the following groups: '{0}'".format( groups ))
                if group in [usergroup.name for usergroup in session.assoc_user.groups]:
                    return f(self, *method_args, **method_kwargs)

            return EResp( STATUS.NOT_AUTHORIZED, "This action requires privileges you do not possess.", None )
        return _impl
    return require_privilege


class GroupLifeCycleController:
    def __init__(self, context_sensitive=True):
        # False is root
        self.session_aware = context_sensitive
        if self.session_aware:
            self.session_controller = SessionLifeCycleController()


#    @require_active_session
    @require_access_level( group=idma_conf.administration['admin_group'] )
    def get_all_groups( self ):
        groups = GroupModel.query.all()
        return EResp( STATUS.SUCCESS, "Dumping ALL groups.", group_schema.dumps( groups ) )

    @require_access_level( group=idma_conf.administration['admin_group'] )
    def create_group(self, name ):
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
    def add_user_to_group(self, user_id, group_id ):
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
    def remove_user_from_group(self, user_id, group_id):
        group_association = GroupMembershipModel.query.filter_by( assoc_uid=user_id, group_id=group_id ).first()
        if group_association is not None:
            resp_attache = json.dumps( group_association.to_dict(), indent=4, sort_keys=True )
            db.session.delete( group_association )
            db.session.commit()

            return EResp( STATUS.SUCCESS, "UID '{0}' removed from GID '{1}'".format( user_id, group_id ), None )
        else:
            return EResp( STATUS.NOT_FOUND, "UID '{0}' is not in GID '{1}'!".format( user_id, group_id ), None )

    @require_access_level( group=idma_conf.administration['admin_group'] )
    def get_associated_groups(self, user_id ):
        user = UserModel.query.get( user_id )

        if user is not None:
            resp_attach = group_schema.dumps( user.groups )
            return EResp( STATUS.SUCCESS, "Groups found for user.", resp_attach )
        else:
            return EResp( STATUS.NOT_FOUND, "User ID is not found.", None )

    @require_access_level( group=idma_conf.administration['admin_group'] )
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

    @require_access_level( group=idma_conf.administration['admin_group'] )
    def get_group_members( self, id ):
        group = GroupModel.query.filter_by( id=id ).first()

        if group is not None:
            members = group.members
            resp_attache = user_schema.dumps( members )
            return EResp( STATUS.SUCCESS, "Group members found.", resp_attache )
        else:
            return EResp( STATUS.NOT_FOUND, "No group found.", None )

    @require_access_level( group=idma_conf.administration['admin_group'] )
    def update_group_details( self, gid, group_name ):
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
