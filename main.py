import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from flask import Flask, request
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema, SQLAlchemySchema, auto_field
from sqlalchemy import exc
from UserLifecycle.Models import *
from UserLifecycle.Schemas import *
from Core.Shared.DB import db
from Core.Shared.API import create_api
from Core.Shared.APP import create_app

app = create_app('config.py')
api = create_api( app )







@api.route('/user', methods=['GET', 'POST'])
@api.route('/user/username/<username>', methods=['GET'])
@api.route('/user/id/<user_id>', methods=['GET', 'DELETE'])
class UserRoute(Resource):
    def get( self, username=None, user_id=None ):
        # retrieve one or all users
        if username is not None:
            users = UserModel.query.filter_by( username=username )
        elif user_id is not None:
            users = UserModel.query.filter_by( id=user_id )
        else:
            users = UserModel.query.all()

        return user_schema.dump( users )

    @api.expect( user_creation_schema( api ) )
    @api.response(201, 'User Created.')
    @api.response(409, 'User already exists.')
    def post(self):
        # create a user

        json_data = request.json

        user = UserModel(
            username=json_data['username'],
            email=json_data['email'],
            password=json_data['password']
        )
        db.session.add( user )

        try:
            db.session.commit()
        except exc.IntegrityError as err:
            db.session.rollback()
            if err.orig.args[0] == 1062:
                return {"error": "User already exists."}, 409

        return user_schema.dump( [ user ] ), 201

    def delete(self):
        # disable a user
        json_data = request.json

        user = UserModel.query.filter_by( id=user_id )


if __name__ == '__main__':
    app.run()
