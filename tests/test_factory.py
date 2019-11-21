import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.dirname(path.dirname(path.abspath(__file__))) ) ) )
import unittest
import json
from datetime import datetime
from app import app, db
from app.models import File, Rol, User
from config import Config
from flask_jwt_extended import (create_access_token, create_refresh_token)

class TestConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'mysql://prueba:123456@flask-mariadb/flask-test'

class TestFactory(unittest.TestCase):
	path = '/'
	def setUp(self):
		app.config.from_object(TestConfig)
		db.session.remove()
		db.drop_all()
		self.app = app.test_client()
		db.create_all()
		data = []
		data.append(File(filename="default.png"))
		data.append(Rol(descripcion="administrador"))
		db.session.add_all(data)
		db.session.commit()
		rolAdm =  Rol.query.filter_by(descripcion="administrador").first()
		administrador = User(
			username="admin",
			nombre = "Super",
			apellido = "admin",
			email = "admin@piradesktest.com",
			rol_id = rolAdm.id,
			ultimo_acceso = datetime.utcnow()
		)
		administrador.set_password("admin")
		db.session.add(administrador)
		db.session.commit()
		self.user_data = self.login_refresh()
		headers = {
			'Authorization': 'Bearer {}'.format(self.user_data["access_token"])
		}
		self.headers = headers
	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_get_page(self):
		response = self.app.get(self.path, content_type = 'application/json', headers=self.headers)
		self.assertEqual(response.status_code, 200)	
	
	#### helper methods ####
	def login_refresh(self):
		data = {
			"username":"admin", 
			"password":"admin"
		}
		response = self.app.post('/login', content_type = 'application/json', data = json.dumps(data))
		return response.json

	def tearDown(self):
		db.session.remove()
		db.drop_all()