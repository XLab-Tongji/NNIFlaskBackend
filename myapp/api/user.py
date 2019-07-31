from flask_restful import Resource, request
from myapp.models.UserConfig import UserConfig
import os
import json


config = UserConfig()


class User(Resource):

    def get(self):
        jsoninfo = json.loads(request.get_data())
        username = jsoninfo['name']
        isExists = os.path.exists(config.get_userpath_by_username(username))
        if not isExists:
            os.makedirs(config.get_userpath_by_username(username))
        return 'log in success'


