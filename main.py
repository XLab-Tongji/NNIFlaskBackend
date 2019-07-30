from flask import Flask, request,jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import subprocess
import os
import re
import json
from UserConfig import UserConfig

app = Flask(__name__)
CORS(app)
#app.config['UPLOAD_FOLDER'] = '/workspace/data'
app.config['ALLOWED_EXTENSIONS'] = set(['py','yml','txt','json'])
user_config = UserConfig()
#path_nnicreate='nni/examples/trials/mnist/config.yml'
#create_cmd='nnictl create --config'+' '+ path_nnicreate

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    # 这里是demo，实际这么返回响应字符串是不规范的
    return '<h1>Hello nni</h1>'

@app.route('/login', methods=['POST'])
def mkdir():
    print(request.form['name'])
    username = request.form['name']
    isExists=os.path.exists(user_config.get_path_by_username(username))
    if not isExists:
        os.makedirs(user_config.get_path_by_username(username))
    return 'log in success'

@app.route('/saveyml', methods=['POST'])
def upload_yml():
    upload_file = request.files['yml']
    username = request.form['name']
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        upload_file.save(os.path.join(user_config.get_path_by_username(username),filename))
        return jsonify({'status': '0', 'message': 'successyml'})
    else:
        return jsonify({'status': '1', 'message': 'failedyml'})

@app.route('/issaveyml', methods=['POST'])
def is_exist_yml():
    username = request.form['name']
    isExists = os.path.exists(os.path.join(user_config.get_path_by_username(username), 'config.yml'))
    print(user_config.get_path_by_username(username))
    print(isExists)
    if isExists:
        return jsonify({'status': '0', 'message': 'exist config.yml'})
    else:
        return jsonify({'status': '1', 'message': 'no config.yml'})

@app.route('/issavempy', methods=['POST'])
def is_exist_mpy():
    pyfilelist=[]
    username = request.form['name']
    names = os.listdir(user_config.get_path_by_username(username))
    for name in names:
        if name.endswith('.py'):
            pyfilelist.append(list(map(str, name.split(','))))
    return jsonify({'status': '0', 'pyfilelist':pyfilelist })

@app.route('/issavesearchjson', methods=['POST'])
def is_exist_search_json():
    username = request.form['name']
    isExists = os.path.exists(os.path.join(user_config.get_path_by_username(username),'search_space.json'))
    if isExists:
        return jsonify({'status': '0', 'message': 'exist searchjson'})
    else:
        return jsonify({'status': '1', 'message': 'no searchjson'})

@app.route('/savempy', methods=['POST'])
def upload_py():
    username = request.form['name']
    upload_file = request.files['mpy']
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        upload_file.save(os.path.join(user_config.get_path_by_username(username),filename))
        return jsonify({'status': '0', 'message': 'successmpy'})
    else:
        return jsonify({'status': '1', 'message': 'failedmpy'})

@app.route('/savesearchjson', methods=['POST'])
def upload_json():
    username = request.form['name']
    upload_file = request.files['searchjson']
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        upload_file.save(os.path.join(user_config.get_path_by_username(username),filename))
        return jsonify({'status': '0', 'message': 'successsearchjson'})
    else:
        return jsonify({'status': '1', 'message': 'failedsearchjson'})

@app.route('/create', methods=['POST'])
def create():
    username = request.form['name']
    path_nnicreate = os.path.join(user_config.get_path_by_username(username), 'config.yml')
    create_cmd = 'nnictl create --config' + ' ' + path_nnicreate + ' -p ' + user_config.get_port_by_username(username)
    print((create_cmd))
    cm1 = subprocess.Popen(create_cmd, shell=True,
                         stdout=subprocess.PIPE)
    is_create = False
    i = 0
    while True:
        line = cm1.stdout.readline()
        if line== b'\n' or i==50:
            break
        else:
            print(line)
            i = i+1
            line = line.decode('GBK')
            reg = r'The experiment id is (.{8})'
            id = re.findall(reg, line)
            if(id):
               iiname=''.join(id)
               user_config.set_id_by_username(username, iiname)
               is_create = True
    if (is_create):
        if(username=='user_1'):
            return jsonify({'status': '0', 'message': 'user_1任务创建成功！','port':'1100'})
        elif(username=='user_2'):
            return jsonify({'status': '0', 'message': 'user_2任务创建成功！', 'port': '1101'})
        elif(username=='user_3'):
            return jsonify({'status': '0', 'message': 'user_3任务创建成功！', 'port': '1102'})
    else:
        return jsonify({'status': '1', 'message': '任务创建失败！', 'port': 'error'})

@app.route('/stop', methods=['POST'])
def stop():
    username = request.form['name']
    id = user_config.get_id_by_username(username)
    stop_cmd = 'nnictl stop'+ ' '+ id
    cm = subprocess.call(stop_cmd, shell=True)
    if (cm==0):
        return jsonify({'status': '0', 'message': 'Successfully stoped experiment!','experiment_ID': id})
    else:
        return jsonify({'status': '1', 'message': 'Unsuccessfully stoped experiment!','experiment_ID':'error'})

@app.route('/show', methods=['POST'])
def show():
    username = request.form['name']
    id = user_config.get_id_by_username(username)
    show_cmd = 'nnictl experiment show' + ' ' + id
    cm = subprocess.Popen(show_cmd, shell=True,stdout=subprocess.PIPE)
    info=cm.communicate()
    return info

@app.route('/stderr', methods=['POST'])
def stderr():
    username = request.form['name']
    id = user_config.get_id_by_username(username)
    show_cmd = 'nnictl experiment show' + ' ' + id
    cm = subprocess.Popen(show_cmd, shell=True,stdout=subprocess.PIPE)
    info=cm.communicate()
    return info

@app.route('/trialls', methods=['POST'])
def trialls():
    username = request.form['name']
    id = user_config.get_id_by_username(username)
    trialls_cmd = 'nnictl trial ls' + ' ' + id
    cm = subprocess.Popen(trialls_cmd, shell=True,stdout=subprocess.PIPE)
    info=cm.communicate()
    return info

# @app.route('/top', methods=['POST'])
# def top():
#     #os.chdir('C:\\Users\\ThinkPad')
#     top_cmd = 'nnictl top'
#     cm=subprocess.Popen(top_cmd, shell=True,stdout=subprocess.PIPE)
#     infomation=[]
#     while True:
#         line = cm.stdout.readline()
#         if line==b'\n':
#             break
#         else:
#             print(line)
#             line = line.decode('GBK')
#             infomation.append(list(map(str, line.split(','))))
#         jsonArr = jsonify(json.dumps(infomation, ensure_ascii=False))
#         return jsonArr

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
