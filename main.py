import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from Core.Shared.API import create_api
from Core.Shared.APP import create_app
from UserLifecycle.Routes import *

app = create_app('config.py')
api = create_api( app )

api.add_namespace( user_namespace )


if __name__ == '__main__':
    app.run()
