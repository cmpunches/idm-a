import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from Core.Shared.APP import create_app
from Core.UserLifecycle.Engine import *
from Core.UserLifecycle.StorageModels import *
from Core.GroupLifecycle.Engine import *
import json


app = create_app('Config.py')


def add_dummy_users():
    with app.app_context():
        # add users
        user_controller = UserLifeCycleController()

        admin_user = user_controller.create_user(
            username='admin',
            email='admin@silogroup.org',
            password='admin',
            first_name="Mister",
            last_name="Admin"
        )

        guest_user = user_controller.create_user(
            username='guest',
            email='guest@silogroup.org',
            password='guest',
            first_name="Misses",
            last_name="Guest"
        )

        lame_user = user_controller.create_user(
            username='delete_me',
            email='delete_me@silogroup.org',
            password='deleteme',
            first_name='delete',
            last_name='me'
        )

        print( admin_user )
        print( guest_user )
        print( lame_user )


if __name__=='__main__':
    add_dummy_users()