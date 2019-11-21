# coding=utf-8
#!/usr/bin/python3

import unittest
import json
from datetime import datetime
from tests.test_factory import TestFactory
from app import db
from app.models import Client

class ClientTest(TestFactory):
	def setUp(self):
		TestFactory.setUp(self)
		
		self.path = '/client'

	def test_post_page(self):
		data = {
			"username": "prueba",
			"nombre": "prueba",
			"apellido": "prueba",
			"email": "prueba@prueba.com",
			"rol_id": 1,
			"password": "Admin00?"
		}
		response = self.app.post(self.path, content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		self.assertEqual(response.status_code, 201)
	
	def test_view_page(self):
		response = self.app.get(self.path + '/1', content_type = 'application/json', headers=self.headers)
		self.assertEqual(response.status_code, 200)
	
	def test_put_page(self):
		data = {
			"username": "admin",
			"nombre": "admin",
			"apellido": "prueba123434",
			"email": "admin@piradesktest.com",
			"rol_id": 1,
			"password": "Admin00?",
			"activo": 1
		}
		response = self.app.put(self.path + '/1', content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		self.assertEqual(response.status_code, 201)
	
	def test_patch_page(self):
		data = {
			"email": "admin12@piradesktest.com",
			"password": "Admin11?"
		}
		response = self.app.patch(self.path + '/1', content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		self.assertEqual(response.status_code, 201)


	
if __name__ == "__main__":
	unittest.main()


