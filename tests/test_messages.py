# coding=utf-8
#!/usr/bin/python3

import unittest
import json
from datetime import datetime
from tests.test_factory import TestFactory
from app import db
from app.models import Message, Ticket, State, Priority, Department, Client

class MessageTest(TestFactory):
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
		message = Message(
			body 				 = "fgkljhdfkljhgklfgjhkldfjhdk",
			privado 		 = False,
			ticket_id 	 = 1,
			from_user_id = 1,
			to_user_id   = None,
		)
		db.session.add(message)
		db.session.commit()
		self.path = '/messages'

	def test_post_page(self):
		data = {
			"body" 				 : "dfsfjd 3454loak k345",
			"privado" 		 : False,
			"ticket_id" 	 : 1,
			"from_user_id" : 1,
			"to_user_id"   : None,
		}
		response = self.app.post(self.path, content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		self.assertEqual(response.status_code, 201)
	
	def test_view_page(self):
		response = self.app.get(self.path + '/1', content_type = 'application/json', headers=self.headers)
		self.assertEqual(response.status_code, 200)
	
	def test_put_page(self):
		data = {
			"body" 				 : "dfsfjd 3454loak k",
			"privado" 		 : False,
			"ticket_id" 	 : 1,
			"from_user_id" : 1,
			"to_user_id"   : None,
		}
		response = self.app.put(self.path + '/1', content_type = 'application/json', data = json.dumps(data), headers=self.headers)
		self.assertEqual(response.status_code, 201)

	
if __name__ == "__main__":
	unittest.main()


