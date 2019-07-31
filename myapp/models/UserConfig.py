import os


class UserConfig(object):
    __instance = None

    def __init__(self):
        self.username2port = {}
        self.username2id = {}
        # self.path = "/Users/xuawai/Temp/nni"
        self.path = '/workspace/data'
        self.ports = set()
        self.ports.add('8080')
        self.ports.add('8081')
        self.ports.add('8082')

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(UserConfig, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def get_port_by_username(self, username):
        if username in self.username2port.keys():
            return self.username2port[username]
        if len(self.ports) > 0:
            port = self.ports.pop()
            self.username2port[username] = port
            return port
        else:
            return 'no available port'

    def get_external_port_by_inner_port(self, port):
        mapping = {'8080':'1100', '8081':'1101', '8082':'1102'}
        return mapping[port]

    def release_port_by_username(self, username):
        port = self.username2port[username]
        self.username2port.pop(username)
        self.username2id.pop(username)
        self.ports.add(port)

    def set_id_by_username(self, username, id):
        self.username2id[username] = id

    def get_id_by_username(self, username):
        return self.username2id[username]

    def get_userpath_by_username(self, username):
        return os.path.join(self.path, username)

    def get_ymlpath_by_username(self,username):
        return os.path.join(self.path, username,'config.yml')

    def get_jsonpath_by_name(self,username):
        return os.path.join(self.path, username, 'search_space.json')

