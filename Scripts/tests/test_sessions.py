import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from Core.Shared.APP import create_app
from Core.UserLifecycle.Engine import *
from Core.SessionLifecycle.Engine import *
from Core.UserLifecycle.StorageModels import *
from Core.GroupLifecycle.Engine import *
import json


app = create_app('config.py')

def populate_sessions():
    with app.app_context():
        session_controller = SessionLifeCycleController()

        response = session_controller.create_session( uid=1 )
        print(response)


if __name__=='__main__':
    populate_sessions()