from Core.UserLifecycle.IO_Schemas import *
from Core.Shared.Config import *
from Core.Shared.ResponseSchema import *

from sqlalchemy import exc

import smtplib, ssl, re


class UserLifeCycleController:
    def __init__(self, context_sensitive=True):
        # False is root -- bypasses access control checks in group and requires no session
        self.session_aware=context_sensitive

    def user_data_valid(self, user):
        if not ( re.search( idma_conf.user_security['email_pattern'], user.email ) ):
            print("Bad email.")
            return False
        if not ( re.search( idma_conf.user_security['username_pattern'], user.username ) ):
            print("Bad username.")
            return False
        if not ( re.search( idma_conf.user_security['password_pattern'], user.password ) ):
            print("Bad password.")
            return False
        if not ( re.search( idma_conf.user_security['name_pattern'], user.first_name ) ):
            print("Bad first name.")
            return False
        if not ( re.search( idma_conf.user_security['name_pattern'], user.last_name ) ):
            print("Bad last name.")
            return False
        return True

    def get_all_users( self, token ):
        users = UserModel.query.all()
        return EResp( STATUS.SUCCESS, "Dumping ALL users.", user_schema.dumps( users ) )

    def get_user_by_uid( self, user_id ):
        user = UserModel.query.filter_by( id=user_id ).first()
        return EResp( STATUS.SUCCESS, "Found the user.", user_schema.dumps( [ user ] ) )

    def get_user_by_username( self, username ):
        user = UserModel.query.filter_by( username=username ).first()
        if user is not None:
            return EResp( STATUS.SUCCESS, "Found the user.", user_schema.dumps( [ user ] ) )
        else:
            return EResp( STATUS.DATA_CONFLICT, "User '{0}' does not exist.".format( username ), None )

    def get_user_by_email( self, email ):
        user = UserModel.query.filter_by( email=email ).first()
        if user is not None:
            return EResp( STATUS.SUCCESS, "Found the user.", user_schema.dumps( [ user ] ) )
        else:
            return EResp( STATUS.DATA_CONFLICT, "User '{0}' does not exist.".format( username ), None )

    def create_user( self, username, email, password, first_name, last_name, context=None ):
        # add context checks

        user = UserModel(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        if not self.user_data_valid(user):
            return EResp( STATUS.FAILURE, "One or more bad user values.", user_schema.dumps( [ user ] ) )

        db.session.add(user)

        try:
            db.session.commit()
        except exc.IntegrityError as err:
            db.session.rollback()
            if err.orig.args[0] == 1062:
                return EResp( STATUS.DATA_CONFLICT, "User with a unique attribute already exists.  Check username and email.", user_schema.dumps( [ user ] ) )
            else:
                return EResp( STATUS.FAILURE, "Couldn't create the user.  Report this.", user_schema.dumps( [ user ] ) )

        self.require_email_validation( user.email )

        return EResp( STATUS.SUCCESS, "User successfully created.", user_schema.dumps( [ user ] ) )

    def update_user_details( self, user_id, email, username, first_name, last_name ):

        user = UserModel.query.get( user_id )

        if user is not None:

            user.username=username
            user.first_name=first_name
            user.last_name=last_name

            try:
                db.session.commit()

                if user.email != email:
                    user.email = email
                    db.session.commit()
                    self.require_email_validation( email )
            except:
                return EResp(
                    STATUS.FAILURE,
                    "User detail update did not complete successfully.  Report this.",
                    user_schema.dumps( [ user ] )
                )
        else:
            return EResp( STATUS.DATA_CONFLICT, "The user does not exist!", None )

        return EResp(
            STATUS.SUCCESS,
            "User details updated for user '{0}'.".format( user.username ),
            user_schema.dumps( [ user ] )
        )

    def update_user_password( self, user_id, password ):

        user = UserModel.query.get( user_id )

        if user is not None:
            if user.password != password:
                user.password = password
                try:
                    db.session.commit()
                except:
                    return EResp(
                        STATUS.FAILURE,
                        "User password update did not complete successfully.  Report this.",
                        user_schema.dumps( [ user ] )
                    )
        else:
            return EResp( STATUS.DATA_CONFLICT, "The user does not exist!", None )

        return EResp(
            STATUS.SUCCESS,
            "Password updated for user '{0}'.".format( user.username ),
            user_schema.dumps( [ user ] )
        )

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

        self.send_validation_email( email, user_validation.code )

        return EResp( STATUS.SUCCESS, "Email validation is now required for that email address.", user_validation )

    def validate_email_code(self, code):
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

        return EResp(
            STATUS.SUCCESS,
            "The email '{0}' has now been verified.".format( email ),
            user_schema.dumps( [ user ] )
        )

    def send_validation_email(self, recipient, code):
        user = UserModel.query.filter_by( email=recipient ).first()

        url = "{0}/user/verify_email/{1}".format(
            BASE_API_MASK,
            code
        )

        message = """From: {0} <{1}> 
To: {2} {5} <{3}>
Reply-To: {1}
Subject: Your {0} Verification URL

Dear {2},

Thanks for signing up on {0} with the username '{6}'.

To get started, you'll need to verify your email address.

Your activation URL is:
{4}

By clicking the above link, your email will be verified.

Regards,
The {0} Team.
        """.format(
            SITE_NAME,
            email_sender,
            user.first_name,
            recipient,
            url,
            user.last_name,
            user.username
        )


        # create a secure SSL context
        # whatever that means
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL( SMTP_SERVER, SMTP_PORT, context=context ) as server:
            server.login( SMTP_USER, SMTP_PASSWORD )
            server.sendmail( email_sender, recipient, message )
