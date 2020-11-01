from Core.Shared.APP import create_app
from Core.Shared.DB import create_db


app = create_app('config.py')
db = create_db( app )

with app.app_context():
    print("We're in app context.  Stuff should be deleted.")
    db.drop_all()
    db.session.commit()

