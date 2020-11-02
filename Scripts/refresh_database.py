from Core.Shared.APP import create_app
from Core.UserLifecycle.StorageModels import *
import time

app = create_app('config.py')

admin_user = UserModel(username='admin', email='smed_admin@silogroup.org', password='smed')
guest_user = UserModel(username='guest', email='guest@silogroup.org', password='guest')

admin_user_validation = EmailValidationModel(email=admin_user.email)
guest_user_validation = EmailValidationModel(email=guest_user.email)

with app.app_context():
    # drop everything
    db.drop_all()
    db.session.commit()

    # regenerate table structures
    db.create_all()
    db.session.commit()

    # add users
    db.session.add(admin_user)
    db.session.add(guest_user)
    db.session.commit()

    # setup pending validation entries
    db.session.add(admin_user_validation)
    db.session.commit()

    time.sleep(3)

    db.session.add(guest_user_validation)
    db.session.commit()

    exit(0)