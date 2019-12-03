# coding=utf-8
#!/usr/bin/python3

import unittest
import json
from datetime import datetime
from tests.test_factory import TestFactory
from app import db
from app.models import Priority

class ClientTest(TestFactory):
	def setUp(self):
		TestFactory.setUp(self)
		priority = Priority(
			descripcion = "baja",
		)
		db.session.add(priority)
		db.session.commit()
		self.path = '/priorities'

	def test_post_page(self):
		data = {
			"descripcion": "media",
			"respuesta":1,
			"resuelto":1,
			"escalable": True
		}
		response = self.app.post(self.path, content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		self.assertEqual(response.status_code, 201)
	
	def test_view_page(self):
		response = self.app.get(self.path + '/1', content_type = 'application/json', headers=self.headers)
		self.assertEqual(response.status_code, 200)
	
	def test_put_page(self):
		data = {
			"descripcion": "baja",
			"respuesta":0,
			"resuelto":0,
			"escalable": True
		}
		response = self.app.put(self.path + '/1', content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		self.assertEqual(response.status_code, 201)

	def test_delete_page(self):
		response = self.app.delete(self.path + '/1', content_type = 'application/json',  headers=self.headers)
		self.assertEqual(response.status_code, 204)

	
if __name__ == "__main__":
	unittest.main()


