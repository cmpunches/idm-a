from Core import *
from Core.SessionLifecycle.Engine import *
from functools import wraps

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
                if method_kwargs['context'] is not None:
                    print("DBUG: Context was provided to the call. ('{0}')".format(method_kwargs['context']))
                    session = SessionLifeCycleController.get_session_object( method_kwargs['context'] )
                    if session is None:
                        return EResp( STATUS.NOT_AUTHORIZED, "This action requires privileges you do not have.", None)
                    user = session.assoc_user
                    print("DBUG: Associated user with this session is '{0}'.".format(user.username))
                    groups = [usergroup.name for usergroup in session.assoc_user.groups]
                    print("DBUG: This user belongs to the following groups: '{0}'".format( groups ))
                    if group in [usergroup.name for usergroup in session.assoc_user.groups]:
                        print("DBUG: Permitting action.")
                        return f(self, *method_args, **method_kwargs)
                else:
                    return EResp( STATUS.NOT_AUTHORIZED, "This action requires privileges you do not have.", None )

            return EResp( STATUS.NOT_AUTHORIZED, "This action requires privileges you do not have.", None )
        return _impl
    return require_privilege
