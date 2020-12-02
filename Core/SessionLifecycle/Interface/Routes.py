from Core.SessionLifecycle.Engine import *
from Core.UserLifecycle.Engine import *
from Core.GroupLifecycle.Engine import *
from Core.UserLifecycle.StorageModels import *
from Core.SessionLifecycle.IO_Schemas import *

from flask_restplus import Namespace, Resource
from flask import request

session_namespace = Namespace('session', description="Session Management Functions")

session_controller = SessionLifeCycleController()


@session_namespace.route( 's' )
class SessionPortfolioRoute(Resource):
    @session_namespace.expect( session_creation_schema( session_namespace ) )
    def post(self):
        # create a session
        json_data = request.json

        # either a username OR email
        user_handle = json_data['user']
        password = json_data['password']

        response = session_controller.create_session( handle=user_handle, password=password )

        if response.status == STATUS.SUCCESS:
            return response.to_json(), 200
        if response.status == STATUS.NOT_FOUND:
            return response.to_json(), 404

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500

    @session_namespace.doc( security='token' )
    def get(self):
        # dump all sessions
        # classified
        response = session_controller.list_all_sessions()

        if response.status == STATUS.SUCCESS:
            return response.to_json(), 200

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500