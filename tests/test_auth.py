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
	#app = null
	#user_data = null
	def setUp(self):
		app.config.from_object(TestConfig)
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
			'Authorization': 'Bearer {}'.format(self.user_data["refresh_token"])
		}
		self.headers = headers
	
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

class AuthTest(unittest.TestCase):
	def setUp(self):
		app.config.from_object(TestConfig)
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

	def tearDown(self):
		db.session.remove()
		db.drop_all()
	
	def test_login_page(self):
		data = {
			"username":"admin", 
			"password":"admin"
		}
		response = self.app.post('/login', content_type = 'application/json', data = json.dumps(data))
		self.assertEqual(response.status_code, 200)

	
	
	def test_tokenrefresh_page(self):
		data = self.login_refresh()
		refresh_token = data['refresh_token']
		headers = {
			'Authorization': 'Bearer {}'.format(refresh_token)
		}
		response = self.app.post('/token/refresh', content_type = 'application/json', headers=headers, data = {})
		self.assertEqual(response.status_code, 200)
		if(response.status_code==200):
			data = response.json
			self.access_token = data["access_token"]
		
	
	def test_logout(self):
		data = self.login_refresh()
		access_token = data['access_token']
		headers = {
			'Authorization': 'Bearer {}'.format(access_token)
		}
		response = self.app.post('/logout/access', content_type = 'application/json', headers=headers)
		self.assertEqual(response.status_code, 200)
	
	def test_logout_refresh(self):
		data = self.login_refresh()
		refresh_token = data['refresh_token']
		headers = {
			'Authorization': 'Bearer {}'.format(refresh_token)
		}
		response = self.app.post('/logout/refresh', content_type = 'application/json', headers=headers)
		self.assertEqual(response.status_code, 200)
	
	
	#### helper methods ####
	def login_refresh(self):
		data = {
			"username":"admin", 
			"password":"admin"
		}
		response = self.app.post('/login', content_type = 'application/json', data = json.dumps(data))
		return response.json



	
if __name__ == "__main__":
	unittest.main()