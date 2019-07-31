from flask import Blueprint
from flask_restful import Api
from myapp.api.files import YmlFile, PythonFile, JsonFile
from myapp.api.user import User
from myapp.api.nni import ExperimentsStarter, ExperimentsStopper, ExperimentsShow, TrialsShow

def register_views(app):
    api = Api(app)
    api.add_resource(YmlFile, '/yml', endpoint="yml")
    api.add_resource(PythonFile, '/py', endpoint="py")
    api.add_resource(JsonFile, '/json', endpoint="json")

    api.add_resource(User, '/login', endpoint="login")

    api.add_resource(ExperimentsStarter, '/start', endpoint="start")
    api.add_resource(ExperimentsStopper, '/stop', endpoint="stop")
    api.add_resource(ExperimentsShow, '/experiments', endpoint="experiments")
    api.add_resource(TrialsShow, '/trials', endpoint="trials")

def create_blueprint_v1():
    """
    注册蓝图->v1版本
    """
    bp_v1 = Blueprint('v1', __name__)
    register_views(bp_v1)
    return bp_v1