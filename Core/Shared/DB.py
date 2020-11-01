from flask_sqlalchemy import SQLAlchemy


def create_db( app ):
    db = SQLAlchemy()
    db.init_app( app )
    return db