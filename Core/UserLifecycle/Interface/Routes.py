from Core.UserLifecycle.Engine import *
from Core.SessionLifecycle.Engine import *
from flask_restplus import Namespace, Resource
from flask import request, url_for, redirect, send_file

user_namespace = Namespace( 'user', description="User Management Functions." )

user_controller = UserLifeCycleController()
session_controller = SessionLifeCycleController()


# GET|POST /users
@user_namespace.route( 's', methods=['GET', 'POST'] )
class UserPortfolio( Resource ):
    @user_namespace.response( 200, "Users found.")
    @user_namespace.response( 403, "Forbidden context.")
    @user_namespace.response( 500, "General failure.")
    @user_namespace.doc( description="Fetch all users" )
    @user_namespace.doc( security='SESSION_ID' )
    def get( self ):
        # retrieve all users
        response = user_controller.get_all_users( request.headers['SESSION_ID'] )

        if response.status == STATUS.SUCCESS:
            return response.to_json(), 200

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500

    @user_namespace.expect( user_creation_schema( user_namespace ) )
    @user_namespace.response( 201, 'User created.')
    @user_namespace.response( 409, 'User already exists.' )
    @user_namespace.doc( description="Create a user." )
    def post(self):
        # create a user
        json_data = request.json

        response = user_controller.create_user(
            username=json_data['username'],
            email=json_data['email'],
            password=json_data['password'],
            first_name=json_data['first name'],
            last_name=json_data['last name']
        )

        if response.status == STATUS.DATA_CONFLICT:
            return response.to_json(), 409
        if response.status == STATUS.FAILURE:
            return response.to_json(), 500
        if response.status == STATUS.SUCCESS:
            return response.to_json(), 201

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500


@user_namespace.response( 404, "Username is not currently in use." )
@user_namespace.response( 200, "Username found." )
@user_namespace.doc(security='SESSION_ID')
@user_namespace.route( '/username/<username>', methods=['GET'] )
class UsernameRoute( Resource ):
    @user_namespace.doc( description="Returns a user search by username.  This is intended as a convenience feature -- usernames are unique but mutable." )
    def get(self, username ):
        response = user_controller.get_user_by_username( username, context=request.headers['SESSION_ID'] )

        if response.status == STATUS.SUCCESS:
            return response.to_json(), 200
        if response.status == STATUS.DATA_CONFLICT:
            return response.to_json(), 404

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500

# GET|DELETE|PUT /id/$id
@user_namespace.route( '/id/<user_id>', methods=['GET', 'DELETE', 'PUT'] )
class UserIDRoute( Resource ):
    @user_namespace.response( 204, 'User has been disabled.' )
    @user_namespace.response( 409, 'User is already disabled.' )
    @user_namespace.doc( description="Deactivate a user." )
    @user_namespace.doc( security='SESSION_ID')
    def delete( self, user_id ):
        response = user_controller.deactivate_user( user_id, context=request.headers['SESSION_ID'] )

        if response.status == STATUS.SUCCESS:
            return response.to_json(), 204
        if response.status == STATUS.DATA_CONFLICT:
            return response.to_json(), 409
        if response.status == STATUS.FAILURE:
            return response.to_json(), 500

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500

    @user_namespace.expect( user_update_schema( user_namespace ) )
    @user_namespace.doc( description="Update a user's details.  Cannot be used for password modification." )
    @user_namespace.doc( security='SESSION_ID')
    def put( self, user_id ):
        json_data = request.json

        response = user_controller.update_user_details(
            user_id=user_id,
            email=json_data['email'],
            username=json_data['username'],
            first_name=json_data['first name'],
            last_name=json_data['last name'],
            context=request.headers['SESSION_ID']
        )

        if response.status == STATUS.SUCCESS:
            return response.to_json(), 200
        if response.status == STATUS.DATA_CONFLICT:
            return response.to_json(), 403
        if response.status == STATUS.FAILURE:
            return response.to_json(), 500

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500


@user_namespace.expect( password_update_schema( user_namespace ) )
@user_namespace.route( '/id/<user_id>/password', methods=['PUT'] )
class PasswordUpdateRoute(Resource):
    @user_namespace.doc(description="Update a user's password.")
    @user_namespace.doc(security='SESSION_ID')
    def put(self, user_id):
        json_data = request.json

        response = user_controller.update_user_password(
            user_id=user_id,
            password=json_data['password'],
            context=request.headers['SESSION_ID']
        )

        if response.status == STATUS.SUCCESS:
            return response.to_json(), 200
        if response.status == STATUS.DATA_CONFLICT:
            return response.to_json(), 403
        if response.status == STATUS.FAILURE:
            return response.to_json(), 500

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500


@user_namespace.route('/verify_email/<code>')
class EmailValidation(Resource):
    @user_namespace.response( 404, 'Invalid email verification code.' )
    @user_namespace.response( 202, 'The user\'s email is now verified.' )
    @user_namespace.doc( description="Verify a user's email validation code." )
    def get( self, code ):

        response = user_controller.validate_email_code(code=code)

        if response.status == STATUS.FAILURE:
            return response.to_json(), 404
        if response.status == STATUS.SUCCESS:
            return response.to_json(), 202

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500
