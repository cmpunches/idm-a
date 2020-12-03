#!/usr/bin/env python3
# Script that will seed the admin group and admin user.
import argparse
import sys, json

from Core import *


def Main():
    app = create_app()

    parser = argparse.ArgumentParser(
        description="Injects a user into the group configured to manage your IDM/A instance.",
        prog="idma_seeder",
        epilog="Designed and implemented by Chris Punches.\nSILO GROUP, LLC 2020.  ALL RIGHTS RESERVED."
    )

    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument("-u", "--username", help="The username of the new root user.", required=True)
    required_args.add_argument("-e", "--email", help="The email of the new root user.", required=True)
    required_args.add_argument("-p", "--password", help="The password of the new root user.", required=True)
    required_args.add_argument("-f", "--first-name", help="The first name of the new root user.", required=True)
    required_args.add_argument("-l", "--last-name", help="The last name of the new root user.", required=True)

    # handles checks for required args
    args = parser.parse_args()

    with app.app_context():
        gc = GroupLifeCycleController( context_sensitive=False )
        uc = UserLifeCycleController( context_sensitive=False )
        admin_group = idma_conf.administration['admin_group']

        print( "Admin group is '{0}'.".format( admin_group ) )

        # Check if the group exists.  If not, create it.  Bail if anything fails.
        if gc.group_exists( group_name=admin_group ):
            print("Group '{0}' already exists.".format( admin_group ) )
        else:
            print("Group '{0}' does NOT exist.  Preparing to inject group.".format( admin_group ) )
            group_creation_result = gc.create_group( admin_group )
            if group_creation_result.status == STATUS.SUCCESS:
                print("Group injected.")
                group_obj = group_creation_result.attachment
                group = group_schema.loads(group_obj)
            else:
                print( group_creation_result.message )
                exit(1)


        # Create the user.  If it already exists, just add it to the group anyway.
        user_creation_result = uc.create_user(
            username=args.username,
            email=args.email,
            password=args.password,
            first_name=args.first_name,
            last_name=args.last_name
        )

        # create user or determine it already exists, or bail
        if user_creation_result.status == STATUS.SUCCESS:
            print( "Created user '{0}' with email '{1}'.".format( args.username, args.email ) )
        elif user_creation_result.status == STATUS.DATA_CONFLICT:
            print( user_creation_result.message )
        else:
            print( user_creation_result.message )
            exit(1)

        # add user to group
        user_get_result = uc.get_user_by_email( email=args.email )
        user = json.loads( user_get_result.attachment )[0]

        add_user_to_admin_group_result = gc.add_user_to_group( user.id, group.id )

        if add_user_to_admin_group_result.status == STATUS.SUCCESS:
            print("User '{0}' has now been injected into the group '{1}'.".format( user.email, group.name ))
        else:
            print( add_user_to_admin_group_result.message )
            exit(1)


if __name__=='__main__':
    Main()