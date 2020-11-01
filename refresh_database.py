from main import db, create_app


app = create_app('config.py')

with app.app_context():
    print("We're in app context.  Stuff should be deleted.")
    db.drop_all()
    db.session.commit()

