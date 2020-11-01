from flask_restplus import Api

def create_api( app ):
    api = Api()
    api.init_app( app )
    return api