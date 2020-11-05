from Core.UserLifecycle.Engine import *

from flask_restplus import Namespace, Resource
from flask import request, url_for, redirect, send_file

user_namespace = Namespace( 'user', description="User management functions." )
user_controller = UserLifeCycleController()


@user_namespace.route( 's', methods=['GET', 'POST'] )
@user_namespace.route( '/username/<username>', methods=['GET'] )
@user_namespace.route( '/id/<user_id>', methods=['GET', 'DELETE'] )
class UserRoute( Resource ):
    @user_namespace.doc( description="Fetch all users, or just one by username or uid." )
    def get( self, username=None, user_id=None ):
        # retrieve one or all users
        if username is not None:
            response = user_controller.get_user_by_username( username )
        elif user_id is not None:
            response = user_controller.get_user_by_uid( user_id )
        else:
            response = user_controller.get_all_users()

        if response.status == STATUS.SUCCESS:
            return response.to_json(), 200

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500

    @user_namespace.expect( user_creation_schema( user_namespace ) )
    @user_namespace.response( 201, 'User Created.')
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

    @user_namespace.response( 204, 'User has been disabled.' )
    @user_namespace.response( 409, 'User is already disabled.' )
    @user_namespace.doc( description="Deactivate a user." )
    def delete( self, user_id ):
        response = user_controller.deactivate_user( user_id )

        if response.status == STATUS.SUCCESS:
            return response.to_json(), 204
        if response.status == STATUS.DATA_CONFLICT:
            return response.to_json(), 409
        if response.status == STATUS.FAILURE:
            return response.to_json(), 500

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500



@user_namespace.expect( user_update_schema( user_namespace ) )
@user_namespace.route( '/id/<user_id>/details', methods=['PUT'] )
class UserDetailsUpdateRoute( Resource ):
    @user_namespace.expect( user_update_schema( user_namespace ) )
    @user_namespace.doc( description="Update a user's details." )
    def put( self, user_id ):
        json_data = request.json

        response = user_controller.update_user_details(
            user_id=user_id,
            email=json_data['email'],
            username=json_data['username'],
            first_name=json_data['first name'],
            last_name=json_data['last name']
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
    def put(self, user_id):
        json_data = request.json

        response = user_controller.update_user_password(
            user_id=user_id,
            password=json_data['password']
        )

        if response.status == STATUS.SUCCESS:
            return response.to_json(), 200
        if response.status == STATUS.DATA_CONFLICT:
            return response.to_json(), 403
        if response.status == STATUS.FAILURE:
            return response.to_json(), 500

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500


@user_namespace.route('/verify/<code>')
class EmailValidation(Resource):
    @user_namespace.response( 404, 'Invalid email verification code.' )
    @user_namespace.response( 202, 'The user\'s email is now verified' )
    @user_namespace.doc( description="Verify a user's email validation code." )
    def get( self, code ):

        response = user_controller.validate_email_code(code=code)

        if response.status == STATUS.FAILURE:
            return response.to_json(), 404
        if response.status == STATUS.SUCCESS:
            return response.to_json(), 202

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500

