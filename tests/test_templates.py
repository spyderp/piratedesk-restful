# coding=utf-8
#!/usr/bin/python3

import unittest
import json
from datetime import datetime
from tests.test_factory import TestFactory
from app import db
from app.models import Template

class TemplateTest(TestFactory):
	def setUp(self):
		TestFactory.setUp(self)
		data = Template(
			descripcion = "default",
			body = "<div></div>"
		)
		db.session.add(data)
		db.session.commit()
		self.path = '/templates'

	def test_post_page(self):
		data = {
			"descripcion": "dark",
			"body":  "<div class='dark'></div>"
		}
		response = self.app.post(self.path, content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		self.assertEqual(response.status_code, 201)
	
	def test_view_page(self):
		response = self.app.get(self.path + '/1', content_type = 'application/json', headers=self.headers)
		self.assertEqual(response.status_code, 200)
	
	def test_put_page(self):
		data = {
			"descripcion": "default",
			"body":  "<div class='white'></div>"
		}
		response = self.app.put(self.path + '/1', content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		self.assertEqual(response.status_code, 201)

	def test_delete_page(self):
		response = self.app.delete(self.path + '/1', content_type = 'application/json',  headers=self.headers)
		self.assertEqual(response.status_code, 204)

	
if __name__ == "__main__":
	unittest.main()


