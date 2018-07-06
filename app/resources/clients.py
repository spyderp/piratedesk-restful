# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, fields, marshal_with, abort, marshal
from flask_jwt_extended import jwt_required
from app import db
from app.models import Client
from app.commons import roles_required

post_parser = reqparse.RequestParser()
post_parser.add_argument(
	'nombre', 
	location='json', required=True,
	help='Nombre del cliente',
)
post_parser.add_argument(
	'direccion', 
	location='json', 
	help='Dirección del cliente',
)
post_parser.add_argument(
	'telefono', 
	location='json', 
	help='Número de teléfono',
)
post_parser.add_argument(
	'celular', 
	location='json', 
	help='Número celular',
)
post_parser.add_argument(
	'email', 
	location='json', 
	help='Correo eléctronico',
)
post_parser.add_argument(
	'calendar_id', 
	location='json', 
	required=True,
)
get_parser = reqparse.RequestParser()
get_parser.add_argument('type', location='args', help='formato respuesta')

calendar_fiels = {
	'descripcion':fields.String
}
client_fields = {
	'id': fields.Integer,
	'nombre': fields.String,
	'direccion': fields.String,
	'email': fields.String,
	'telefono': fields.String,
	'celular': fields.String,
	'email': fields.String,
	'calendar_id':fields.Integer,
	'calendars':fields.Nested(calendar_fiels)
}

class Clients(Resource):
	@jwt_required
	@roles_required('administrador', 'agente')
	def get(self, client_id=None):
		args = get_parser.parse_args()
		if(not client_id):
			client = Client.query.all()
		else:
			client = Client.query.filter_by(id=client_id).first()
			if(not client):
				abort(404, message="Client {} doesn't exist".format(client_id))
		if(args.type=='list'):
			data = []
			for row in client:
				data.append({'id':row.id, 'text':row.nombre})
		return marshal(client,client_fields)  if not args.type  else data

	@jwt_required
	def delete(self, client_id):
		client = Client.query.filter_by(id=client_id).first()
		if(not client):
				abort(404, message="Client {} doesn't exist".format(client_id))
		db.session.delete(client)
		db.session.commit()
		return '', 204

	@jwt_required
	@marshal_with(client_fields)
	def post(self):
		args = post_parser.parse_args()
		client = Client(
			nombre 		= args.nombre,
			direccion = args.direccion,
			telefono 	= args.telefono,
			celular  	= args.celular,
			email  		= args.email,
			calendar_id = args.calendar_id   
		)
		db.session.add(client)
		db.session.commit()
		return client,201

	@jwt_required
	@marshal_with(client_fields)
	def put(self, client_id):
		args = post_parser.parse_args()
		client = Client.query.filter_by(id=client_id).first()
		if(not client):
				abort(404, message="Client {} doesn't exist".format(client_id))
		if(not args.nombre):
			abort(404, message="El nombre es requerido no puede esta vacio")
		client.direccion   = args.direccion
		client.nombre 		 = args.nombre,
		client.telefono 	 = args.telefono,
		client.celular  	 = args.celular,
		client.email  		 = args.email
		client.calendar_id = args.calendar_id   
		db.session.commit()
		return client,201

