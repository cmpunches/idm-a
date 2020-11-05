import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from Core.Shared.APP import create_app
from Core.UserLifecycle.Engine import *
from Core.UserLifecycle.StorageModels import *

import json
app = create_app('config.py')


def add_dummy_users():
    with app.app_context():
        # add users
        user_controller = UserLifeCycleController()
        print( json.dumps( user_controller.create_user( username='admin', email='admin@silogroup.org', password='admin', first_name="Mister", last_name="Admin" ).to_json(), indent=4, sort_keys=True ) )
        print( json.dumps( user_controller.create_user( username='guest', email='guest@silogroup.org', password='guest', first_name="Misses", last_name="Guest" ).to_json(), indent=4, sort_keys=True ) )
        exit(0)


if __name__=='__main__':
    add_dummy_users()