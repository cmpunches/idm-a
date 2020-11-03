from flask_restplus import Namespace, Resource
from flask import request
from Core.UserLifecycle.Engine import *

user_namespace = Namespace( 'user', description="User management functions." )
user_controller = UserLifeCycleController()


@user_namespace.route('', methods=['GET', 'POST'])
@user_namespace.route('/username/<username>', methods=['GET'])
@user_namespace.route('/id/<user_id>', methods=['GET', 'DELETE'])
class UserRoute(Resource):
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

        return { "general": "failure" }, 444

    @user_namespace.expect( user_creation_schema( user_namespace ) )
    @user_namespace.response(201, 'User Created.')
    @user_namespace.response(409, 'User already exists.')
    def post(self):
        # create a user
        json_data = request.json

        response = user_controller.create_user(
            username=json_data['username'],
            email=json_data['email'],
            password=json_data['password']
        )

        if response.status == STATUS.DATA_CONFLICT:
            return response.to_json(), 409
        if response.status == STATUS.FAILURE:
            return response.to_json(), 500
        if response.status == STATUS.SUCCESS:
            return response.to_json(), 201

    @user_namespace.response(204, 'User has been disabled.')
    @user_namespace.response(409, 'User is already disabled.')
    def delete( self, user_id ):
        # disable a user

        response = user_controller.deactivate_user( user_id )

        if response.status == STATUS.SUCCESS:
            return response.to_json(), 204
        if response.status == STATUS.DATA_CONFLICT:
            return response.to_json(), 409
        if response.status == STATUS.FAILURE:
            return response.to_json(), 500


@user_namespace.route('/verify/<code>')
class EmailValidation(Resource):
    @user_namespace.response( 404, 'Invalid email verification code.' )
    @user_namespace.response( 202, 'The user\'s email is now verified' )
    def get( self, code ):

        response = user_controller.validate_email( code=code )

        print("hitfarm")
        if response.status == STATUS.FAILURE:
            return response.to_json(), 404
        if response.status == STATUS.SUCCESS:
            return response.to_json(), 202
