
import os
class UserConfig(object):
    __instance = None

    def __init__(self):
        self.username_id = {}

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(UserConfig, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def get_port_by_username(self, username):# 名称
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

    def get_path_by_username(self, username):
        return os.path.join('/workspace/data', username)


# class user(User):
#     def __init__(self):
#         self
#     def inforgive(self,user_name):
#         self.name = user_name  # 名称
#         self.user_road = os.path.join('/workspace/data', user_name)
#         if(self.name=='user_1'):
#             self.port = '8080'  # 接口
#         elif(self.name=='user_2'):
#             self.port='8081'
#         else:
#             self.port='8082'
#
#     def giveexperiment_id(self, id):
#         self.experiment_id=id
