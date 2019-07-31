from flask_restful import Resource, request
from werkzeug.utils import secure_filename
from myapp.models.UserConfig import UserConfig
import os
from flask import jsonify
import json


config = UserConfig()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in set(['py','yml','txt','json'])


class YmlFile(Resource):

   def post(self):
       upload_file = request.files['yml']
       username = request.form['name']
       if upload_file and allowed_file(upload_file.filename):
           filename = secure_filename(upload_file.filename)
           upload_file.save(os.path.join(config.get_userpath_by_username(username), filename))
           return jsonify({'status': '0', 'message': 'successyml'})
       else:
           return jsonify({'status': '1', 'message': 'failedyml'})

   def get(self):
       username = "user1"
       path = config.get_ymlpath_by_username(username)
       isExists = os.path.exists(path)
       if isExists:
           return jsonify({'status': '0', 'message': 'exist config.yml'})
       else:
           return jsonify({'status': '1', 'message': 'no config.yml'})

class PythonFile(Resource):

   def post(self):
       pyfilelist = []
       jsoninfo = json.loads(request.get_data())
       username = jsoninfo['name']
       names = os.listdir(config.get_userpath_by_username(username))
       for name in names:
           if name.endswith('.py'):
               pyfilelist.append(list(map(str, name.split(','))))
       return jsonify({'status': '0', 'pyfilelist': pyfilelist})

   def get(self):
       username = request.form['name']
       upload_file = request.files['mpy']
       if upload_file and allowed_file(upload_file.filename):
           filename = secure_filename(upload_file.filename)
           upload_file.save(os.path.join(config.get_userpath_by_username(username), filename))
           return jsonify({'status': '0', 'message': 'successmpy'})
       else:
           return jsonify({'status': '1', 'message': 'failedmpy'})

class JsonFile(Resource):

   def post(self):
       username = request.form['name']
       upload_file = request.files['searchjson']
       if upload_file and allowed_file(upload_file.filename):
           filename = secure_filename(upload_file.filename)
           upload_file.save(os.path.join(config.get_userpath_by_username(username), filename))
           return jsonify({'status': '0', 'message': 'successsearchjson'})
       else:
           return jsonify({'status': '1', 'message': 'failedsearchjson'})

   def get(self):
       jsoninfo = json.loads(request.get_data())
       username = jsoninfo['name']
       isExists = os.path.exists(config.get_jsonpath_by_name(username))
       if isExists:
           return jsonify({'status': '0', 'message': 'exist searchjson'})
       else:
           return jsonify({'status': '1', 'message': 'no searchjson'})