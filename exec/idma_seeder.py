#!/usr/bin/env python3
# Script that will seed the admin group and admin user.
import argparse
import sys, json

from Core import *


def deserialize( schema, jsonobj ):
    jd = json.loads( jsonobj )
    return schema.load( jd, session=db.session )

def Main():
    app = create_app()

    parser = argparse.ArgumentParser(
        description="Injects a user into the group configured to manage your IDM/A instance.",
        prog="python3 -m exec.idma_seeder",
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

        print( "Target IDMA administrator group is '{0}'.".format( admin_group ) )
        group_creation_result = gc.create_group( admin_group )

        if group_creation_result.status == STATUS.SUCCESS:
            group = deserialize( group_schema, group_creation_result.attachment )[0]
            print( "Group named '{0}' injected.".format( group.name ) )
        elif group_creation_result.status == STATUS.DATA_CONFLICT:
            print( "Group named '{0}' already exists.  Fetching group object.".format( admin_group ) )
            group_fetch_result = gc.get_group_by_name( admin_group )
            if group_fetch_result.status == STATUS.SUCCESS:
                group = deserialize( group_schema, group_fetch_result.attachment )[0]
                print( "Group found with ID '{0}'.".format( group.id ) )
            else:
                # group already exists and could not be fetched
                print( group_fetch_result.message )
                exit(1)
        else:
            # Unhandled results of group creation failure
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
            user = deserialize(user_schema, user_creation_result.attachment)[0]
            print( "Created user '{0}' with email '{1}'.".format( user.username, user.id ) )
        elif user_creation_result.status == STATUS.DATA_CONFLICT:
            print( user_creation_result.message )
            exit(1)
        else:
            print( user_creation_result.message )
            exit(1)

        add_user_to_admin_group_result = gc.add_user_to_group( user.id, group.id )

        if add_user_to_admin_group_result.status == STATUS.SUCCESS:
            print("User with current email address of '{0}' and an ID of '{2}' has been injected into the group '{1}'.".format( user.email, group.name, user.id ))
        else:
            print( add_user_to_admin_group_result.message )
            exit(1)


if __name__=='__main__':
    Main()
else:
    print("Consult the documentation.")