# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, fields, marshal_with, abort, marshal
from flask_jwt_extended import jwt_required
from app import db
from app.models import Ticket
from app.commons import roles_required, DateTimeLatinFormat
import json
post_parser = reqparse.RequestParser()
post_parser.add_argument(
	'titulo', 
	location='json', required=True,
	help='Titulo',
)
post_parser.add_argument(
	'content', 
	location='json', required=True,
	help='contenido',
)
post_parser.add_argument(
	'keys', 
	location='json', 
)
post_parser.add_argument(
	'client_id', 
	location='json', 
)
post_parser.add_argument(
	'department_id', 
	location='json', 
)
post_parser.add_argument(
	'priority_id', 
	location='json', 
)
post_parser.add_argument(
	'user_id', 
	location='json', 
)
get_parser = reqparse.RequestParser()
get_parser.add_argument('find', location='args', help='for find')
get_parser.add_argument('page', location='args', help='paging', type=int)
get_parser.add_argument('order', location='args', help='order')
client_fields = {
	'id': fields.Integer,
	'nombre': fields.String,
	'direccion': fields.String,
	'email': fields.String,
	'telefono': fields.String,
	'celular': fields.String,
	'email': fields.String,
}

department_fields = {
	'descripcion': fields.String,
}
priority_fields = {
	'id': fields.Integer,
	'descripcion': fields.String,
	'respuesta': fields.Integer,
	'resuelto': fields.Integer,
	'escalable': fields.Boolean,
}
state_fields = {
	'descripcion': fields.String,
}
user_fields = {
	'username': fields.String,
	'nombre': fields.String,
	'apellido': fields.String,
	'email': fields.String,
}
ticket_fields = {
	'id': fields.Integer,
	'titulo': fields.String,
	'keys': fields.String,
	'content': fields.String,
	'creado':DateTimeLatinFormat,
	'modificado':DateTimeLatinFormat,
	'client_id':fields.Integer,
	'department_id':fields.Integer,
	'state_id':fields.Integer,
	'user_id':fields.Integer,
	'clients':fields.Nested(client_fields),
	'departments':fields.Nested(department_fields),
	'priorities':fields.Nested(priority_fields),
	'states':fields.Nested(state_fields),
	'users':fields.Nested(user_fields),

}

class Tickets(Resource):
	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(ticket_fields)
	def get(self, ticket_id=None):
		if(not ticket_id):
			args = get_parser.parse_args()
			if(not args.find):
				ticket = Ticket.query.filter(Ticket.state_id.notin_([4,5])).all() if(not args.page) else Ticket.query.paginate(args.page, 18, False).items
			else:
				query = []
				filtro = json.loads(args.find)
				if(filtro.has_key('descripcion')):
					query.append(Ticket.titulo.like('%{}%'.format(filtro['descripcion'])))
				if(filtro.has_key('estado')):
					query.append(Ticket.state_id.in_(filtro['estado']))
				if(filtro.has_key('prioridad')):
					query.append(Ticket.priority_id.in_(filtro['prioridad']))
				if(filtro.has_key('departamento')):
					query.append(Ticket.department_id.in_(filtro['departamento']))
				if(filtro.has_key('fecha_desde')):
					query.append(Ticket.creado>='{}-{}-{}'.format(filtro['departamento']['year'],filtro['departamento']['month'],filtro['departamento']['day']))
				if(filtro.has_key('fecha_hasta')):
					query.append(Ticket.creado>='{}-{}-{}'.format(filtro['departamento']['year'],filtro['departamento']['month'],filtro['departamento']['day']))
				if(len(query)>1):
					ticket = Ticket.query.filter(db.or_(*query)).all() if(not args.page) else Ticket.query.filter(db.or_(*query)).paginate(args.page, 18, False).items
				else:
					ticket = Ticket.query.filter(*query).all() if(not args.page) else Ticket.query.filter(*query).paginate(args.page, 18, False).items
		else:
			ticket = Ticket.query.filter_by(id=ticket_id).first()
			if(not ticket):
				abort(404, message="Ticket {} doesn't exist".format(ticket_id))
		return ticket

	@jwt_required
	def delete(self, client_id):
		ticket = Ticket.query.filter_by(id=ticket_id).first()
		if(not ticket):
				abort(404, message="Ticket {} doesn't exist".format(ticket_id))
		db.session.delete(ticket)
		db.session.commit()
		return '', 204

	@jwt_required
	@marshal_with(ticket_fields)
	def post(self):
		args = post_parser.parse_args()
		ticket = Ticket(
			titulo        = args.titulo,
			content       = args.content,
			key           = args.key,
			client_id     = args.client_id,
			department_id = args.department_id,
			priority_id   = args.priority_id,
			state_id      = args.state_id,
			user_id	      = args.user_id
		)
		db.session.add(ticket)
		db.session.commit()
		return ticket,201

	@jwt_required
	@marshal_with(ticket_fields)
	def put(self, ticket_id):
		args = post_parser.parse_args()
		ticket = Ticket.query.filter_by(id=ticket_id).first()
		if(not ticket):
				abort(404, message="Ticket {} doesn't exist".format(ticket_id))
		if(not args.nombre):
			abort(404, message="El nombre es requerido no puede esta vacio")
		ticket.titulo        = args.titulo
		ticket.content       = args.content
		ticket.client_id     = args.client_id
		ticket.department_id = args.department_id
		ticket.priority_id   = args.priority_id
		ticket.state_id      = args.state_id
		db.session.commit()
		return ticket,201