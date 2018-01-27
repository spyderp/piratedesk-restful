from flask import Flask
from flask_restful import Api
from config import Config, ConfigCors
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)
cors = CORS(app, resources={r"/*": {"origins": ConfigCors.origins}})

from app import models
from app.resources.auth import Auth, TokenRefresh, LogoutAccess, LogoutRefresh
from app.resources.clients import Clients
from app.resources.departments import Departments
from app.resources.rols import Rols
from app.resources.users import Users


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedToken.is_jti_blacklisted(jti)


api.add_resource(Auth, '/login')
api.add_resource(Clients, '/clients', '/clients/<client_id>')
api.add_resource(Departments, '/departments', '/departments/<department_id>')
api.add_resource(Rols, '/rols', '/rols/<rol_id>')
api.add_resource(Users, '/users', '/users/<user_id>')
api.add_resource(LogoutAccess, '/logout/access')
api.add_resource(LogoutRefresh, '/logout/refresh')
api.add_resource(TokenRefresh, '/token/refresh')