from flask import Flask
from myapp import register_blueprints

flask_app = Flask(__name__)

def init_app(app):
    register_blueprints(app)

init_app(flask_app)

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5000, debug=True)