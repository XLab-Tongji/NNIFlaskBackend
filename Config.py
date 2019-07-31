from UserConfig import UserConfig
import os
class Config():
    def __init__(self):
        self.user_path=''
    def get_userpath_by_username(self, username):
        return os.path.join('/workspace/data', username)
    def get_ymlpath_by_username(self,username):
        return os.path.join('/workspace/data', username,'config.yml')
    def get_jsonpath_by_name(self,username):
        return os.path.join('/workspace/data', username, 'search_space.json')