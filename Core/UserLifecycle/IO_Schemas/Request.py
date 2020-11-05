from flask_restplus import fields


def user_creation_schema(api):
    # user representation on post for the docs
    return api.model(
        "User Creation Schema",
        {
            "username": fields.String(description="The username for the new user."),
            "email": fields.String(description="The email address of the new user."),
            "password": fields.String(description="The password of the new user."),
            "first name": fields.String(description="The first name of the user."),
            "last name": fields.String(description="The last name of the user.")
        }
    )

def user_update_schema(api):
    return api.model(
        "User Update Schema",
        {
            "username": fields.String(description="The username for the new user."),
            "email": fields.String(description="The email address of the new user."),
            "first name": fields.String(description="The first name of the user."),
            "last name": fields.String(description="The last name of the user.")
        }
    )

def password_update_schema(api):
    return api.model(
        "Password Update Schema",
        {
            "password": fields.String( description="The new password of the existing user." )
        }
    )