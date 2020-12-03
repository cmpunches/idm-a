
# Execution context MUST be the project root directory
from Core import *


app = create_app()

api = create_api( app )

api.add_namespace( user_namespace )
api.add_namespace( group_namespace )
api.add_namespace( session_namespace )

if __name__ == '__main__':
    app.run()
