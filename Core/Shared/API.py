from flask_restplus import Api

authorizations = {
    'SESSION_ID': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'SESSION_ID'
    }
}

def create_api( app ):
    api = Api(
        title='IDM/A Backend Interface',
        version='1.0',
        description='Backend API for the IDM/A system.',
        authorizations=authorizations
    )
    api.init_app( app )
    return api