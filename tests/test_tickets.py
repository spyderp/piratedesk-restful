# coding=utf-8
#!/usr/bin/python3

import unittest
import json
from datetime import datetime
from tests.test_factory import TestFactory
from app import db
from app.models import Ticket, Client, Department, Priority, State

class TicketTest(TestFactory):
	def setUp(self):
		TestFactory.setUp(self)
		data = []
		data.append(State(descripcion = "abierto"))
		data.append(State(descripcion = "cerrado"))
		data.append(Priority(descripcion = "baja"))
		data.append(Priority(descripcion = "Alta"))
		data.append(Department(descripcion = "default"))
		data.append(Client(nombre = "default"))
		db.session.add_all(data)
		db.session.commit()
		data = Ticket(
			titulo = "prueba",
			content = """My money's in that office, right? If she start giving me some bullshit about it ain't there, and we got to go someplace 
			else and get it, I'm gonna shoot you in the head then and there. Then I'm gonna shoot that bitch in the kneecaps, find out where my 
			goddamn money is. She gonna tell me too. Hey, look at me when I'm talking to you, motherfucker. You listen: we go in there, and that
			 nigga Winston or anybody else is in there, you the first motherfucker to get shot. You understand?""",
			email = "prueba@probando.com", 
			client_id = 1, 
			department_id = 1, 
			priority_id = 1, 
			state_id = 1, 
			user_id = 1
		)
		db.session.add(data)
		db.session.commit()
		self.path = '/tickets'

	def test_post_page(self):
		data = {
			"titulo":  "prueba2",
			"content":  """My money's in that office, right? If she start giving me some bullshit about it ain't there, and we got to go someplace 
			else and get it, I'm gonna shoot you in the head then and there. Then I'm gonna shoot that bitch in the kneecaps, find out where my 
			goddamn money is. She gonna tell me too. Hey, look at me when I'm talking to you, motherfucker. You listen: we go in there, and that
			 nigga Winston or anybody else is in there, you the first motherfucker to get shot. You understand?""",
			"email":  "prueba@probando.com", 
			"client_id":  1, 
			"department_id":  1, 
			"priority_id":  1, 
			"user_id":  1
		}
		response = self.app.post(self.path, content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		self.assertEqual(response.status_code, 201)
	
	def test_view_page(self):
		response = self.app.get(self.path + '/1', content_type = 'application/json', headers=self.headers)
		self.assertEqual(response.status_code, 200)
	
	def test_put_page(self):
		data = {
			"titulo":  "prueba",
			"content":  """My money's in that office, right? If she start giving me some bullshit about it ain't there, and we got to go someplace 
			else and get it, I'm gonna shoot you in the head then and there.""",
			"email":  "prueba@probando.com", 
			"client_id":  1, 
			"department_id":  1, 
			"priority_id":  2, 
			"user_id":  1
		}
		response = self.app.put(self.path + '/1', content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		self.assertEqual(response.status_code, 201)

	def test_patch_state(self):
		data = {
			"type":  1,
			"state_id":  2, 
		}
		response = self.app.patch(self.path + '/1', content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		self.assertEqual(response.status_code, 200)
	
	def test_patch_asign(self):
		data = {
			"type":  0,
			"ticket_id":  1,
			"user_id": 1 ,
			"edit": False
		}
		response = self.app.patch(self.path + '/1', content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		self.assertEqual(response.status_code, 200)
	def test_patch_upload(self):
		data = {
			"type":  2,
			"file_id":  1,
		}
		response = self.app.patch(self.path + '/1', content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		self.assertEqual(response.status_code, 200)
	
	def test_patch_removef(self):
		data = {
			"type":  2,
			"file_id":  1,
		}
		self.app.patch(self.path + '/1', content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		data = {
			"type":  3,
			"file_id":  1,
		}
		response = self.app.patch(self.path + '/1', content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		self.assertEqual(response.status_code, 200)

	def test_get_filter1(self):
		data = {
			"find": json.dumps({"descripcion": "prueba"})
		}
		response = self.app.get(self.path  , content_type = 'application/json', headers=self.headers, query_string = data)
		self.assertEqual(response.status_code, 200)	

	def test_get_filter2(self):
		data = {
			"find": json.dumps({"estado": 1})
		}
		response = self.app.get(self.path  , content_type = 'application/json', headers=self.headers, query_string = data)
		self.assertEqual(response.status_code, 200)	

	def test_get_filter3(self):
		data = {
			"find": json.dumps({"prioridad": 1})
		}
		response = self.app.get(self.path  , content_type = 'application/json', headers=self.headers, query_string = data)
		self.assertEqual(response.status_code, 200)	
	
	def test_get_filter4(self):
		data = {
			"find": json.dumps({"departamento": 1})
		}
		response = self.app.get(self.path  , content_type = 'application/json', headers=self.headers, query_string = data)
		self.assertEqual(response.status_code, 200)	
	
	def test_get_filter5(self):
		data = {
			"find": json.dumps({"fecha_desde": { "day": 24, "month": 11, "year": 2019 }})
		}
		response = self.app.get(self.path  , content_type = 'application/json', headers=self.headers, query_string = data)
		self.assertEqual(response.status_code, 200)	
	
	def test_get_filter6(self):
		data = {
			"find": json.dumps({"fecha_hasta": { "day": 27, "month": 11, "year": 2019 }})
		}
		response = self.app.get(self.path  , content_type = 'application/json', headers=self.headers, query_string = data)
		self.assertEqual(response.status_code, 200)	
	
	def test_get_filter7(self):
		data = {
			"find": json.dumps({
				"descripcion": "prueba", 
				"prioridad": 1
			})
		}
		response = self.app.get(self.path  , content_type = 'application/json', headers=self.headers, query_string = data)
		self.assertEqual(response.status_code, 200)	
	
	def test_get_filter8(self):
		data = {
			"find": json.dumps({
				"fecha_desde": { "day": 24, "month": 11, "year": 2019 },
				"fecha_hasta": { "day": 27, "month": 11, "year": 2019 }
			})
		}
		response = self.app.get(self.path  , content_type = 'application/json', headers=self.headers, query_string = data)
		self.assertEqual(response.status_code, 200)
	
	def test_delete_page(self):
		response = self.app.delete(self.path + '/1', content_type = 'application/json',  headers=self.headers)
		self.assertEqual(response.status_code, 204)
	


	
if __name__ == "__main__":
	unittest.main()


