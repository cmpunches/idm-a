from flask_restplus import fields


def user_creation_schema( api ):
    # user representation on post for the docs
    return api.model(
        "User Creation Schema",
        {
            "username": fields.String(description="The username for the new user."),
            "email": fields.String(description="The email address of the new user."),
            "password": fields.String(description="The password of the new user.")
        }
    )

