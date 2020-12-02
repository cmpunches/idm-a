import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from Core.SessionLifecycle.StorageModels.Models import SessionModel
from Core.GroupLifecycle.StorageModels.Models import GroupModel, GroupMembershipModel
from Core.UserLifecycle.StorageModels.Models import UserModel, EmailValidationModel


from Core.Shared.APP import create_app
from Core.Shared.DB import db


app = create_app( 'Core/Shared/config.py' )


def refresh_database():
    with app.app_context():
        # drop everything
        db.drop_all()
        db.session.commit()

        # regenerate table structures
        db.create_all()
        db.session.commit()


if __name__=='__main__':
    refresh_database()