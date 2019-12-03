# coding=utf-8
#!/usr/bin/python3

import unittest
import json
from datetime import datetime
from tests.test_factory import TestFactory
from app import db
from app.models import Department

class DepartmentTest(TestFactory):
	def setUp(self):
		TestFactory.setUp(self)
		data = []
		data.append(Department(descripcion="padre", user_id=1))
		data.append(Department(descripcion="hijo", user_id=1, parent_id=1))
		db.session.add_all(data)
		db.session.commit()
		self.path = '/departments'

	def test_post_page(self):
		data = {
			"descripcion": "CARIMAÑOLA SA",
			"parent_id": 2,
			"user_id": 1
		}
		response = self.app.post(self.path, content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		self.assertEqual(response.status_code, 201)
	
	def test_view_page(self):
		response = self.app.get(self.path + '/1', content_type = 'application/json', headers=self.headers)
		self.assertEqual(response.status_code, 200)
	
	def test_put_page(self):
		data = {
			"descripcion": "super_hijo",
			"parent_id": 1,
			"user_id": 1
		}
		response = self.app.put(self.path + '/2', content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		self.assertEqual(response.status_code, 201)

	def test_delete_page(self):
		response = self.app.delete(self.path + '/1', content_type = 'application/json',  headers=self.headers)
		self.assertEqual(response.status_code, 404)

	def test_delete2_page(self):
		response = self.app.delete(self.path + '/2', content_type = 'application/json',  headers=self.headers)
		self.assertEqual(response.status_code, 204)

	
if __name__ == "__main__":
	unittest.main()


