from flask import Flask, request,jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import subprocess
import os
import re
import json
from NNIFlaskBackend.User import User

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = '/workspace/data'
app.config['ALLOWED_EXTENSIONS'] = set(['py','yml','txt','json'])

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
    global path_nni
    global r_user
    request.form.get('name')
    if(request.form['name']=='user_1'):
        r_user=User('user_1','8080')
    elif(request.form['name']=='user_2'):
        r_user = User('user_2', '8081')
    elif (request.form['name'] == 'user_3'):
        r_user = User('user_3', '8082')
    #print(request.form.get('name'))
    isExists = os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],request.form['name']))
    path_nni=os.path.join(app.config['UPLOAD_FOLDER'],request.form['name'])
    if not isExists:
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'],request.form['name']))
    return 'log in success'

@app.route('/saveyml', methods=['POST'])
def upload_yml():
    global path_nni
    upload_file = request.files['yml']
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        upload_file.save(os.path.join(path_nni,filename))
        return jsonify({'status': '0', 'message': 'successyml'})
    else:
        return jsonify({'status': '1', 'message': 'failedyml'})

@app.route('/issaveyml', methods=['POST'])
def isexistyml():
    global r_user
    print(os.path.join(app.config['UPLOAD_FOLDER'],r_user.name,'config.yml'))
    isExists = os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], r_user.name,'config.yml'))
    if isExists:
        return jsonify({'status': '0', 'message': 'exist config.yml'})
    else:
        return jsonify({'status': '1', 'message': 'no config.yml'})

@app.route('/issavempy', methods=['POST'])
def isexistmpy():
    pyfilelist=[]
    global r_user
    names = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'],r_user.name))
    for name in names:
        if name.endswith('.py'):
            pyfilelist.append(list(map(str, name.split(','))))
        #jsonArr = jsonify(json.dumps(pyfilelist, ensure_ascii=False))
    return jsonify({'status': '0', 'pyfilelist':pyfilelist })

@app.route('/issavesearchjson', methods=['POST'])
def isexistsearchjson():
    global r_user
    isExists = os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], r_user.name,'search_space.json'))
    if isExists:
        return jsonify({'status': '0', 'message': 'exist searchjson'})
    else:
        return jsonify({'status': '1', 'message': 'no searchjson'})

@app.route('/savempy', methods=['POST'])
def upload_py():
    upload_file = request.files['mpy']
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        upload_file.save(os.path.join(path_nni,filename))
        return jsonify({'status': '0', 'message': 'successmpy'})
    else:
        return jsonify({'status': '1', 'message': 'failedmpy'})

@app.route('/savesearchjson', methods=['POST'])
def upload_json():
    upload_file = request.files['searchjson']
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        upload_file.save(os.path.join(path_nni,filename))
        #print(path_nni)
        #print(os.path.join(path_nni,filename))
        return jsonify({'status': '0', 'message': 'successsearchjson'})
    else:
        return jsonify({'status': '1', 'message': 'failedsearchjson'})

@app.route('/create', methods=['POST'])
def create():
    #os.chdir('C:\\Users\\ThinkPad')
    global iiname
    path_nnicreate = os.path.join(path_nni, 'config.yml')
    create_cmd = 'nnictl create --config' + ' ' + path_nnicreate + ' -p ' + r_user.port
    print((create_cmd))
    cm1 = subprocess.Popen(create_cmd, shell=True,
                         stdout=subprocess.PIPE)
    #line = cm1.stdout.readline()
    i=0
    while True:
        line = cm1.stdout.readline()
        #if line == b'\x1b[0m\r\n'or i==50:
        if line== b'\n' or i==50:
            break
        #print(line)
        else:
            print(line)
            i=i+1
            #encode_type = chardet.detect(line)
            line = line.decode('GBK')
            reg = r'The experiment id is (.{8})'
            #reg = r'(The experiment id is .{8})'
            id = re.findall(reg, line)
            if(id):
               iiname=''.join(id)
               print(iiname)
    if (iiname):
        if(r_user.name=='user_1'):
            return jsonify({'status': '0', 'message': 'user_1任务创建成功！','port':'1100'})
        elif(r_user.name=='user_2'):
            return jsonify({'status': '0', 'message': 'user_2任务创建成功！', 'port': '1101'})
        else:
            return jsonify({'status': '0', 'message': 'user_3任务创建成功！', 'port': '1102'})
    else:
        return jsonify({'status': '1', 'message': '任务创建失败！', 'port': 'error'})

@app.route('/stop', methods=['POST'])
def stop():
    #os.chdir('C:\\Users\\ThinkPad')
    global iiname
    stop_cmd = 'nnictl stop'+ ' '+ iiname
    cm = subprocess.call(stop_cmd, shell=True)
    if (cm==0):
        return jsonify({'status': '0', 'message': 'Successfully stoped experiment!','experiment_ID':iiname})
    else:
        return jsonify({'status': '1', 'message': 'Unsuccessfully stoped experiment!','experiment_ID':'error'})

@app.route('/show', methods=['POST'])
def show():
    #os.chdir('C:\\Users\\ThinkPad')
    global iiname
    show_cmd = 'nnictl experiment show' + ' ' + iiname
    cm = subprocess.Popen(show_cmd, shell=True,stdout=subprocess.PIPE)
    info=cm.communicate()
    return info

@app.route('/stderr', methods=['POST'])
def stderr():
    #os.chdir('C:\\Users\\ThinkPad')
    global iiname
    show_cmd = 'nnictl experiment show' + ' ' + iiname
    cm = subprocess.Popen(show_cmd, shell=True,stdout=subprocess.PIPE)
    info=cm.communicate()
    return info

@app.route('/trialls', methods=['POST'])
def trialls():
    #os.chdir('C:\\Users\\ThinkPad')
    global iiname
    trialls_cmd = 'nnictl trial ls' + ' ' + iiname
    cm = subprocess.Popen(trialls_cmd, shell=True,stdout=subprocess.PIPE)
    info=cm.communicate()
    return info

@app.route('/top', methods=['POST'])
def top():
    #os.chdir('C:\\Users\\ThinkPad')
    top_cmd = 'nnictl top'
    cm=subprocess.Popen(top_cmd, shell=True,stdout=subprocess.PIPE)
    infomation=[]
    while True:
        line = cm.stdout.readline()
        if line==b'\n':
            break
        else:
            print(line)
            line = line.decode('GBK')
            infomation.append(list(map(str, line.split(','))))
        jsonArr = jsonify(json.dumps(infomation, ensure_ascii=False))
        return jsonArr

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
