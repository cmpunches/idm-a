from Core.GroupLifecycle.Engine import *

from flask_restplus import Namespace, Resource
from flask import request
from functools import wraps

group_namespace = Namespace('group', description="Group Management Functions")

group_controller = GroupLifeCycleController()


@group_namespace.route( 's', methods=['GET', 'DELETE', 'POST'] )
class GroupPortfolioRoute(Resource):
    @group_namespace.doc( security="SESSION_ID")
    @group_namespace.response( 200, "Groups found." )
    @group_namespace.response( 500, "General failure." )
    @group_namespace.response( 401, "Not authorized." )
    @group_namespace.doc( description="List all groups.")
    def get(self):
        context = request.headers.get('SESSION_ID')
        print("Interface: Context is: {0}".format( context ))
        response = group_controller.get_all_groups(context=context)

        if response.status == STATUS.SUCCESS:
            return response.to_json(), 200
        if response.status == STATUS.FAILURE:
            return response.to_json(), 500
        if response.status == STATUS.NOT_AUTHORIZED:
            return response.to_json(), 401

        response.message = "General Failure.  This is a bug and should be reported."
        return response.to_json(), 500


    @group_namespace.expect( group_delete_schema( group_namespace ) )
    @group_namespace.response( 404, "Group not found." )
    @group_namespace.response( 204, "Group deleted." )
    @group_namespace.doc( description="Delete a group." )
    def delete( self ):
        json_data = request.json

        response = group_controller.delete_group( id=json_data['id'] )

        if response.status == STATUS.NOT_FOUND:
            return response.to_json(), 404
        if response.status == STATUS.SUCCESS:
            return response.to_json(), 204

        return response.to_json(), 500

    @group_namespace.response( 201, "Group created." )
    @group_namespace.response( 409, "Group already exists." )
    @group_namespace.expect( group_creation_schema( group_namespace ) )
    @group_namespace.doc( description="Create a group.")
    def post(self):
        json_data = request.json

        response = group_controller.create_group(
            name=json_data['groupname']
        )

        if response.status == STATUS.DATA_CONFLICT:
            return response.to_json(), 409
        if response.status == STATUS.FAILURE:
            return response.to_json(), 500
        if response.status == STATUS.SUCCESS:
            return response.to_json(), 201

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500


@group_namespace.route( '/id/<group_id>' )
class GroupMembershipRoute(Resource):
    @group_namespace.response( 409, "That user is already in that group." )
    @group_namespace.response( 404, "Either that user or that group (or both) do(es) not exist." )
    @group_namespace.response( 201, "User successfully added to group." )
    @group_namespace.expect(group_membership_update_schema(group_namespace))
    @group_namespace.doc( description='Add a user to a group.' )
    def post( self, group_id ):
        json_data = request.json

        response = group_controller.add_user_to_group( user_id=json_data['uid'], group_id=group_id)

        if response.status == STATUS.DATA_CONFLICT:
            return response.to_json(), 409
        if response.status == STATUS.NOT_FOUND:
            return response.to_json(), 404
        if response.status == STATUS.SUCCESS:
            return response.to_json(), 201

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500

    @group_namespace.response( 404, "Either that user or that group (or both) do(es) not exist." )
    @group_namespace.response( 201, "User successfully removed from group." )
    @group_namespace.expect(group_membership_update_schema(group_namespace))
    @group_namespace.doc( description='Remove a user from a group.' )
    def delete(self, group_id ):
        json_data = request.json
        response = group_controller.remove_user_from_group( user_id=json_data['uid'], group_id=group_id )

        if response.status == STATUS.NOT_FOUND:
            return response.to_json(), 404
        if response.status == STATUS.SUCCESS:
            return response.to_json(), 201

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500

    @group_namespace.response( 404, "Group not found." )
    @group_namespace.response( 200, "Found group members." )
    @group_namespace.doc( description='List members of a group.' )
    def get( self, group_id ):
        response = group_controller.get_group_members( id=group_id )

        if response.status == STATUS.NOT_FOUND:
            return response.to_json(), 404
        if response.status == STATUS.SUCCESS:
            return response.to_json(), 200

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500

    @group_namespace.expect( group_update_schema( group_namespace ) )
    @group_namespace.doc( description='Modify the details of a group.' )
    def put(self, group_id ):
        json_data = request.json

        response = group_controller.update_group_details( gid=group_id, group_name=json_data['groupname'] )

        if response.status == STATUS.NOT_FOUND:
            return response.to_json(), 404
        if response.status == STATUS.SUCCESS:
            return response.to_json(), 201

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500


@group_namespace.route( 's/user_id/<user_id>' )
class UserMembershipRoute(Resource):
    @group_namespace.doc( description='List all groups that a user is a member of.' )
    def get(self, user_id ):
        response = group_controller.get_associated_groups( user_id=user_id )

        if response.status == STATUS.NOT_FOUND:
            return response.to_json(), 404
        if response.status == STATUS.SUCCESS:
            return response.to_json(), 200

        response.message = "General failure.  This is a bug and should be reported."
        return response.to_json(), 500
