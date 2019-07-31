from flask_restful import Resource, request
from werkzeug.utils import secure_filename
from myapp.models.UserConfig import UserConfig
import os
from flask import jsonify


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
           return jsonify({'status': '0', 'message': 'successful'})
       else:
           return jsonify({'status': '1', 'message': 'failed'})

   def get(self):
       username = request.args.get("name")
       path = config.get_ymlpath_by_username(username)
       isExists = os.path.exists(path)
       if isExists:
           return jsonify({'status': '0', 'message': 'exist'})
       else:
           return jsonify({'status': '1', 'message': 'non-exist'})


class PythonFile(Resource):

   def post(self):
       username = request.form['name']
       upload_file = request.files['py']
       if upload_file and allowed_file(upload_file.filename):
           filename = secure_filename(upload_file.filename)
           upload_file.save(os.path.join(config.get_userpath_by_username(username), filename))
           return jsonify({'status': '0', 'message': 'successful'})
       else:
           return jsonify({'status': '1', 'message': 'failed'})

   def get(self):
       pyfilelist = []
       username = request.args.get("name")
       names = os.listdir(config.get_userpath_by_username(username))
       for name in names:
           if name.endswith('.py'):
               pyfilelist.append(list(map(str, name.split(','))))
       return jsonify({'status': '0', 'pyfilelist': pyfilelist})


class JsonFile(Resource):

   def post(self):
       username = request.form['name']
       upload_file = request.files['json']
       if upload_file and allowed_file(upload_file.filename):
           filename = secure_filename(upload_file.filename)
           upload_file.save(os.path.join(config.get_userpath_by_username(username), filename))
           return jsonify({'status': '0', 'message': 'successful'})
       else:
           return jsonify({'status': '1', 'message': 'failed'})

   def get(self):
       username = request.args.get("name")
       isExists = os.path.exists(config.get_jsonpath_by_name(username))
       if isExists:
           return jsonify({'status': '0', 'message': 'exists'})
       else:
           return jsonify({'status': '1', 'message': 'non-exist'})