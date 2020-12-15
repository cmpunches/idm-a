from Core import *
from Core.SessionLifecycle.Engine import *
from Core.Shared.ResponseSchema import *
from functools import wraps

not_authorized_response = EResp( STATUS.NOT_AUTHORIZED, "This action requires privileges you do not have.", None )
no_session_response = EResp( STATUS.NOT_AUTHORIZED, "This action requires an active session.", None )


# Decorator to require just an active session.  This allows you to create public/private.
def require_active_session(method):
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):
        if self.session_aware:
            print("DBUG: The Auth layer is enabled.")
            if 'context' in method_kwargs.keys():
                if method_kwargs['context'] is not None:
                    print("DBUG: Context was provided to the call. ('{0}')".format(method_kwargs['context']))
                    if not SessionLifeCycleController.session_is_active(token=method_kwargs['context']):
                        print("DBUG: The context is an inactive or non-existent session.")
                        return no_session_response
                    else:
                        print("DBUG: The context is an active session.")
                        return method(self, *method_args, **method_kwargs)
            else:
                print("DBUG: Auth layer is enabled but no context provided.")
                return no_session_response
        else:
            print("DBUG The auth layer is not enabled.  Disregarding context.")
            return method(self, *method_args, **method_kwargs)
        return no_session_response
    return _impl


# Decorate to require a specific group membership.  This allows granular access control.  Allows the administrator group
# to bypass.
def require_access_level(group):
    def require_privilege(f):
        @wraps(f)
        def _impl(self, *method_args, **method_kwargs):
            if self.session_aware:
                print("DBUG: Auth layer is enabled.")
                print("DBUG: This method requires a context from a user in group '{0}'.".format(group))
                if method_kwargs['context'] is not None:
                    print("DBUG: Context was provided to the call. ('{0}')".format(method_kwargs['context']))
                    session = SessionLifeCycleController.get_session_object( method_kwargs['context'] )
                    if session is None:
                        return not_authorized_response
                    user = session.assoc_user
                    print("DBUG: Associated user with this session is '{0}'.".format(user.username))
                    groups = [usergroup.name for usergroup in session.assoc_user.groups]
                    print("DBUG: This user belongs to the following groups: '{0}'".format( groups ))
                    if group in groups or idma_conf.administration['admin_group'] in groups:
                        print("DBUG: Permitting action.")
                        return f(self, *method_args, **method_kwargs)
                else:
                    return not_authorized_response
            else:
                # not session aware
                print("DBUG: Auth layer not enabled, permitting action.")
                return f(self, *method_args, **method_kwargs)
            return not_authorized_response
        return _impl
    return require_privilege


# Require that the function being called can only be used to modify the user associated with the calling context.  This
# allows self-maintenance features for the users.  Allows the administrator group to bypass.
# Note: This decorator introduced the requirement that the decorated method have the argument 'user_id' to reference the
# id of the target user.
def require_same_user( method ):
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):
        if self.session_aware:
            print( "DBUG: Auth layer is enabled." )
            print( "DBUG: This method requires a context from the same user it is being applied to." )
            if method_kwargs['context'] is not None:
                print("DBUG: Context was provided to the call. ('{0}')".format(method_kwargs['context']))
                session = SessionLifeCycleController.get_session_object( method_kwargs['context'] )
                if session is None:
                    return not_authorized_response
                user = session.assoc_user
                print("DBUG: Associated user with this session is '{0}'.".format(user.username))
                groups = [usergroup.name for usergroup in session.assoc_user.groups]
                print("DBUG: This user belongs to the following groups: '{0}'".format(groups))
                if idma_conf.administration['admin_group'] in groups:
                    print("DBUG: Admin user. Permitting action.")
                    return f(self, *method_args, **method_kwargs)
                if user.id == method_kwargs['user_id']:
                    print("DBUG: Calling user matches target user.")
                    return method(self, *method_args, **method_kwargs)
            # we are session aware, but context is none
            return not_authorized_response
        else:
            print("DBUG: Not session aware, disregarding context.")
            return method(self, *method_args, **method_kwargs)
    return _impl
