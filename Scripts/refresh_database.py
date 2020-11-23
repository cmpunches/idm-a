import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from Core.Shared.APP import create_app

from Core.UserLifecycle.StorageModels import *
from Core.GroupLifecycle.StorageModels import *
from Core.SessionLifecycle.StorageModels import *

app = create_app('config.py')


def refresh_database():
    with app.app_context():
        # drop everything
        db.drop_all()
        db.session.commit()

        # regenerate table structures
        db.create_all()
        db.session.commit()


if __name__=='__main__':
    refresh_database()