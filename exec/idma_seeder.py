#!/usr/bin/env python3
# Script that will seed the admin group and admin user.
import argparse
import sys
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from Core.Shared.APP import create_app

app = create_app()


def Main():

    parser = argparse.ArgumentParser(
        description="Injects a user into the group configured to manage your IDM/A instance.",
        prog="idma_seeder",
        epilog="Designed and implemented by Chris Punches.\nSILO GROUP, LLC 2020.  ALL RIGHTS RESERVED."
    )

    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument( "-c", "--config_file", help="The config file path for your IDMA instance.", required=True )

    required_args.add_argument( "-u", "--username", help="The username of the new root user.", required=True )
    required_args.add_argument( "-e", "--email", help="The email of the new root user.", required=True )
    required_args.add_argument( "-p", "--password", help="The password of the new root user.", required=True )
    required_args.add_argument( "-f", "--first-name", help="The first name of the new root user.", required=True )
    required_args.add_argument( "-l", "--last-name", help="The last name of the new root user.", required=True )

    # handles checks for required args
    args = parser.parse_args()

    print("can create user in group '{0}'".format( get_config_group( args.config_file ) ))

if __name__=='__main__':
    Main()