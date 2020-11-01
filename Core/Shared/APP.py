from flask import Flask

def create_app( config_filename ):
    app = Flask( 'smed' )
    app.config.from_pyfile( config_filename )
    return app