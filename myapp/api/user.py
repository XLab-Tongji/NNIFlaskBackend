from flask_restful import Resource, request
from myapp.models.UserConfig import UserConfig
import os


config = UserConfig()


class User(Resource):

    def get(self):
        username = request.args.get("name")
        isExists = os.path.exists(config.get_userpath_by_username(username))
        if not isExists:
            os.makedirs(config.get_userpath_by_username(username))
        return 'log in successfully'


