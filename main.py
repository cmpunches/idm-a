import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

# Execution context MUST be the project root directory

from Core.Shared.API import create_api
from Core.Shared.APP import create_app

from Core.UserLifecycle.Interface import *
from Core.GroupLifecycle.Interface import *
from Core.SessionLifecycle.Interface import *

app = create_app('Core/Shared/config.py')
api = create_api( app )

api.add_namespace( user_namespace )
api.add_namespace( group_namespace )
api.add_namespace( session_namespace )

if __name__ == '__main__':
    app.run()
