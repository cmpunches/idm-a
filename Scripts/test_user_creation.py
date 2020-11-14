import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from Core.Shared.APP import create_app
from Core.UserLifecycle.Engine import *
from Core.UserLifecycle.StorageModels import *
from Core.GroupLifecycle.Engine import *
import json


app = create_app('config.py')


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


def add_groups():
    with app.app_context():
        group_controller = GroupLifeCycleController()

        response = group_controller.create_group( "test_group1" )
        print(response)
        response = group_controller.create_group( "test_group2" )
        print(response)
        response = group_controller.create_group( "test_group3" )
        print(response)


def populate_groups():
    with app.app_context():
        group_controller = GroupLifeCycleController()

        # only 2 users exist, with uid 1 and 2 respectively
        # only one group exists, with gid 1

        # we want to test:
        # adding an existing uid to an existing gid
        response = group_controller.add_user_to_group( group_id=1, user_id=1 )
        print(response)

        # adding a non-existent uid to a non-existent gid
        response = group_controller.add_user_to_group( group_id=3, user_id=3 )
        print(response)

        # adding an existing uid to a non-existent gid
        response = group_controller.add_user_to_group( group_id=3, user_id=1 )
        print(response)

        # adding a non-existent uid to an existing gid
        response = group_controller.add_user_to_group( group_id=1, user_id=3 )
        print(response)


if __name__=='__main__':
    add_dummy_users()
    add_groups()
    populate_groups()