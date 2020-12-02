from flask import Flask, url_for
from Core.Shared.DB import db
from Core.Shared.config import idma_conf

def create_app():
    app = Flask( idma_conf.orientation['site_name'] )
    app.config.from_pyfile( 'Core/Shared/config.py' )

    db.init_app( app )
    return app

