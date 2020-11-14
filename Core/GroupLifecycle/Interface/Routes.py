from Core.GroupLifecycle.Engine import *

from flask_restplus import Namespace, Resource
from flask import request

group_namespace = Namespace('group', description="Group Management Functions")

group_controller = GroupLifeCycleController()


@group_namespace.route( 's', methods=['GET', 'DELETE', 'POST'] )
class GroupRoute( Resource ):
    @group_namespace.doc( description="List all groups.")
    def get(self):
        response = group_controller.get_all_groups()

        if response.status == STATUS.SUCCESS:
            return response.to_json(), 200
        if response.status == STATUS.FAILURE:
            return response.to_json(), 500

        response.message = "General Failure.  This is a bug and should be reported."
        return response.to_json(), 500

    @group_namespace.doc( description="Delete a group.")
    def delete(self):
        return { "not": "implemented" }, 500

    @group_namespace.doc( description="Create a group.")
    def post(self):
        return { "not": "implemented" }, 500


@group_namespace.route( '/name/<group_name>')
class AddUserToGroupRoute( Resource ):
    @group_namespace.doc( description='Add a user to a group.')
    def post( self, group_name ):
        return { "not": "implemented" }, 500

    @group_namespace.doc( description='Remove a user from a group.')
    def delete(self, group_name ):
        return { "not": "implemented" }, 500

    @group_namespace.doc( description='List members of a group.')
    def get( self, group_name ):
        return { "not": "implemented" }, 500

@group_namespace.route( 's/user_id/<user_id>' )
class ListUserGroups( Resource ):
    @group_namespace.doc( description='List all groups that a user is a member of.' )
    def get(self):
        return { "not": "implemented" }, 500