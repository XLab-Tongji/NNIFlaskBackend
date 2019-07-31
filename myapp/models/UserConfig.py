import os
class UserConfig(object):
    __instance = None

    def __init__(self):
        self.username_id = {}
        self.path = "/Users/xuawai/Temp/nni"
        # '/workspace/data'

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(UserConfig, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def get_port_by_username(self, username):
        if(username=='user_1'):
            port = '8080'
        elif(username=='user_2'):
            port = '8081'
        elif(username=='user_3'):
            port = '8082'
        return port

    def set_id_by_username(self, username, id):
        self.username_id[username] = id

    def get_id_by_username(self, username):
        return self.username_id[username]

    def get_userpath_by_username(self, username):
        return os.path.join(self.path, username)

    def get_ymlpath_by_username(self,username):
        return os.path.join(self.path, username,'config.yml')

    def get_jsonpath_by_name(self,username):
        return os.path.join(self.path, username, 'search_space.json')

