from Core.Shared.APP import create_app
from Core.UserLifecycle.Models import *

app = create_app('config.py')

admin_user = UserModel(username='admin', email='smed_admin@silogroup.org', password='smed')
guest_user = UserModel(username='guest', email='guest@silogroup.org', password='guest')

with app.app_context():
    db.drop_all()
    db.session.commit()
    db.create_all()
    db.session.add(admin_user)
    db.session.add(guest_user)
    db.session.commit()
    exit(0)