from flask_restful import Resource, request
from myapp.models.UserConfig import UserConfig
from flask import jsonify
import json
import subprocess
import re


config = UserConfig()


class ExperimentsStarter(Resource):

    def post(self):
        jsoninfo = json.loads(request.get_data())
        username = jsoninfo['name']
        create_cmd = 'nnictl create --config' + ' ' + config.get_ymlpath_by_username(
            username) + ' -p ' + config.get_port_by_username(username)
        print((create_cmd))
        cm1 = subprocess.Popen(create_cmd, shell=True,
                               stdout=subprocess.PIPE)
        is_create = False
        i = 0
        while True:
            line = cm1.stdout.readline()
            if line == b'\n' or i == 50:
                break
            else:
                print(line)
                i = i + 1
                line = line.decode('GBK')
                reg = r'The experiment id is (.{8})'
                id = re.findall(reg, line)
                if (id):
                    iiname = ''.join(id)
                    config.set_id_by_username(username, iiname)
                    is_create = True
        if (is_create):
            return jsonify({'status': '0', 'message': username+'任务创建成功！', 'port': config.get_external_port_by_inner_port(username)})
        else:
            return jsonify(
                {'status': '1', 'message': username + '任务创建失败！', 'port': config.get_port_by_username(username)})


class ExperimentsStopper(Resource):

    def post(self):
        jsoninfo = json.loads(request.get_data())
        username = jsoninfo['name']
        id = config.get_id_by_username(username)
        stop_cmd = 'nnictl stop' + ' ' + id
        cm = subprocess.call(stop_cmd, shell=True)
        if (cm == 0):
            config.release_port_by_username(username)
            return jsonify({'status': '0', 'message': 'Successfully stop the experiment!', 'experiment_ID': id})
        else:
            return jsonify({'status': '1', 'message': 'Failed to stop the experiment!', 'experiment_ID': 'error'})


class ExperimentsShow(Resource):

    def post(self):
        jsoninfo = json.loads(request.get_data())
        username = jsoninfo['name']
        id = config.get_id_by_username(username)
        show_cmd = 'nnictl experiment show' + ' ' + id
        cm = subprocess.Popen(show_cmd, shell=True, stdout=subprocess.PIPE)
        info = cm.communicate()
        return jsonify(json.loads(info[0]))


class TrialsShow(Resource):

    def post(self):
        jsoninfo = json.loads(request.get_data())
        username = jsoninfo['name']
        id = config.get_id_by_username(username)
        trialls_cmd = 'nnictl trial ls' + ' ' + id
        cm = subprocess.Popen(trialls_cmd, shell=True, stdout=subprocess.PIPE)
        info = cm.communicate()
        return jsonify(json.loads(info[0]))