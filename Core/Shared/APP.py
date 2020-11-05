from flask import Flask, url_for
from Core.Shared.DB import db

def create_app( config_filename ):
    app = Flask( 'smed' )
    app.config.from_pyfile( config_filename )

    db.init_app( app )
    return app

