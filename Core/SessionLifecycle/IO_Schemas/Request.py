from flask_restplus import fields


def session_creation_schema( api ):
    # group representation on post for the docs
    return api.model(
        "Session Creation Schema",
        {
            "user": fields.String( description="The email address or username of the user to authenticate."),
            "password": fields.String( description="The password of the user to authenticate." )
        }
    )
