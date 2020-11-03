from Core.UserLifecycle.StorageModels import *
from Core.UserLifecycle.IO_Schemas import *

from sqlalchemy import exc


class UserLifeCycleController:
    def __init__(self):
        pass

    def get_all_users( self ):
        users = UserModel.query.all()
        return EResp( STATUS.SUCCESS, "Dumping ALL users.", user_schema.dumps( users ) )

    def get_user_by_uid( self, user_id ):
        user = UserModel.query.filter_by( id=user_id ).first()
        return EResp( STATUS.SUCCESS, "Found the user.", user_schema.dumps( [ user ] ) )

    def get_user_by_username( self, username ):
        user = UserModel.query.filter_by( username=username ).first()
        return EResp( STATUS.SUCCESS, "Found the user.", user_schema.dumps( [ user ] ) )

    def create_user( self, username, email, password ):
        user = UserModel( username=username, email=email, password=password )
        db.session.add(user)

        try:
            db.session.commit()
        except exc.IntegrityError as err:
            db.session.rollback()
            if err.orig.args[0] == 1062:
                return EResp( STATUS.DATA_CONFLICT, "User already exists.", [ user ] )
            else:
                return EResp( STATUS.FAILURE, "Couldn't create the user.  Report this.", user_schema.dumps( [ user ] ) )
        return EResp( STATUS.SUCCESS, "User successfully created.", user_schema.dumps( [ user ] ) )

    def deactivate_user( self, user_id ):
        user = UserModel.query.get( user_id )
        if user.active:
            user.active = False
        else:
            return EResp( STATUS.DATA_CONFLICT, "User is already disabled.", user_schema.dumps( [ user ] ) )

        db.session.commit()

        return EResp( STATUS.SUCCESS, "User disabled.", user_schema.dumps( [ user ] ) )


    def activate_user(self, user_id ):
        user = UserModel.query.get( user_id )
        if not user.active:
            user.active = True
        else:
            return EResp( STATUS.DATA_CONFLICT, "User is already active.", user_schema.dumps( [ user ] ) )

        db.session.commit()

        return EResp( STATUS.SUCCESS, "User activated.", user_schema.dumps( [ user ] ) )

    def require_email_validation( self, email ):
        user_validation = EmailValidationModel( email=email )

        db.session.add( user_validation )
        try:
            db.session.commit()
        except exc.IntegrityError as err:
            db.session.rollback()
            if err.orig.args[0] == 1062:
                return EResp(STATUS.DATA_CONFLICT, "There was a data conflict.", user_validation )
            else:
                return EResp(STATUS.FAILURE, "Couldn't create the user validation.  Report this.", user_validation )

        return EResp( STATUS.SUCCESS, "Email validation is now required for that email address.", user_validation )

    def validate_email( self, code ):
        # get a validation entry for that code
        validation_entry = EmailValidationModel.query.filter_by( code=code ).first()

        if validation_entry is not None:
            email = validation_entry.email

            # delete the entry in the validation table
            db.session.delete( validation_entry )

            # set the associated user to active
            user = UserModel.query.filter_by( email=email ).first()
            user.verified = True
            db.session.commit()

        else:
            return EResp( STATUS.FAILURE, "Invalid code." )

        return EResp( STATUS.SUCCESS, "The email has now been verified.", user_schema.dumps( [ user ] ) )


    def send_validation_email(self):
        pass