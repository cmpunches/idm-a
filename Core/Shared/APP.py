from flask import Flask, url_for
from Core.Shared.DB import db
from Core.Shared.Config import idma_conf

def create_app():
    app = Flask( idma_conf.orientation['site_name'] )
    app.config.from_pyfile( 'Core/Shared/Config.py' )

    db.init_app( app )
    return app

