from flask_restplus import Api

def create_api( app ):
    api = Api(
        title='SME/D Backend Interface',
        version='1.0',
        description='Backend API for the SME/D system.'
    )
    api.init_app( app )
    return api