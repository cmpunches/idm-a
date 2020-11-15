from flask_restplus import fields


def group_creation_schema( api ):
    # group representation on post for the docs
    return api.model(
        "Group Creation Schema",
        {
            "groupname": fields.String( description="The name of the group to create." )
        }
    )


def group_update_schema( api ):
    return api.model(
        "Group Update Schema",
        {
            "groupname": fields.String( description="The new name of the group." )
        }
    )

def group_membership_update_schema( api ):
    return api.model(
        "Group Membership Update Schema",
        {
            "uid": fields.Integer( description="The user ID to update in the group's membership." )
        }
    )

def group_delete_schema( api ):
    return api.model(
        "Group Deletion Schema",
        {
            "id": fields.Integer( description="The group ID of the group to delete." )
        }
    )