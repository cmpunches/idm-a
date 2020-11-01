from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from UserLifecycle.Models.Models import UserModel

db = SQLAlchemy()


def create_app( config_filename ):
    app = Flask('smed')
    app.config.from_pyfile( config_filename )
    db.init_app(app)
    return app


app = create_app('config.py')

with app.app_context():
    print("We're in app context.  Stuff should be deleted.")
    db.drop_all()
    db.session.commit()

