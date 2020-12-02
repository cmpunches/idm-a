from Core.Shared.config import *
import datetime
from sqlalchemy import or_


class SessionLifeCycleController:
    def __init__(self):
        pass

    # authentication point
    def create_session( self, handle, password ):
        userObj = UserModel.query.filter( or_( UserModel.email == handle, UserModel.username == handle ) ).first()

        not_found_response = EResp( STATUS.NOT_FOUND, "Invalid credentials.", None )

        if userObj is not None:
            if password != userObj.password:
                # even though we found a user, we want to report not found if the password doesn't match to cut down
                # on CRIME
                # not doing this can leak partial account credentials
                return not_found_response

            session = SessionModel( uid=userObj.id )

            db.session.add( session )

            db.session.commit()
            resp_attache = session_schema.dumps( [ session ] )

            return EResp( STATUS.SUCCESS, "Session created.", resp_attache )
        else:
            # supplied identifier for user was invalid for both email and username
            return not_found_response

    # classified
    def list_all_sessions( self ):
        sessions = SessionModel.query.all()
        return EResp( STATUS.SUCCESS, "Dumping ALL sessions.", session_schema.dumps( sessions ) )

    # classified
    def destroy_session( self, token ):
        pass

    # classified
    def list_all_sessions_for_user( self, uid ):
        pass

    # classified
    def destroy_all_sessions_for_user(self, uid ):
        pass

    def session_is_active( self, token ):
        session = SessionModel.query.get( token )

        if session is not None:
            timestamp = session.timestamp
            delta = datetime.now() - datetime.fromisoformat( timestamp )
            if delta.seconds > SESSION_EXPIRY_SECONDS:
                print( "Expiring session with token {0}".format( session.token ) )
                # it's there but it's expired, so it's not active
                # go ahead and delete it and return false
                db.session.delete( session )
                db.session.commit()
                return False
            else:
                # session exists, is associated with token, and is not expired
                return True
        else:
            # session does not exist
            return False

    def return_session_context( self, token ):
        context = None
        if self.session_is_active( token ):
            context = SessionModel.get( token )
            return context
        else:
            return None

