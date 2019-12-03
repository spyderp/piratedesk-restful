# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, fields, marshal_with, abort, marshal
from flask_jwt_extended import jwt_required
from app import db
from app.models import Message
from app.commons import roles_required, DateTimeLatinFormat

post_parser = reqparse.RequestParser()
post_parser.add_argument('body', location='json', required=True, help='cuerpo del mensaje')
post_parser.add_argument('privado', location='json',  help='mensaja privado(booleano)', type=bool)
post_parser.add_argument('ticket_id', location='json', required=True, help='ticket del mensaje')
post_parser.add_argument('from_user_id', location='json', required=True, help='quien lo envia')
post_parser.add_argument('to_user_id', location='json', help='quien lo recibe (solo privado)')

user_fields = {
	'id': fields.Integer,
	'nombre': fields.String,
	'apellido': fields.String
}
message_fields = {
	'id': fields.Integer,
	'body': fields.String, 
	'creado': DateTimeLatinFormat(),
	'privado': fields.Integer,
	'ticket_id': fields.Integer,
	'fromUser': fields.Nested(user_fields),
	'toUser':	  fields.Nested(user_fields),
}

class Messages(Resource):

	@jwt_required
	@marshal_with(message_fields)
	@roles_required('administrador', 'agente')
	def get(self, message_id=None):
		if(not message_id):
			message = Message.query.all()
		else:
			message = Message.query.filter_by(id=message_id).first()
		if(not message):
			abort(404, message="message {} doesn't exist".format(message_id))
		return message,200

	@jwt_required
	@roles_required('administrador')
	def delete(self, message_id):
		message = Message.query.filter_by(id=message_id).first()
		if(not message):
				abort(404, message="message {} doesn't exist".format(message_id))
		db.session.delete(message)
		db.session.commit()
		return '', 204

	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(message_fields)
	def post(self):
		args = post_parser.parse_args()
		message = Message(
			body 				 = args.body,
			privado 		 = args.privado,
			ticket_id 	 = args.ticket_id,
			from_user_id = args.from_user_id,
			to_user_id   = args.to_user_id,
		)
		db.session.add(message)
		db.session.commit()
		return message,201

	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(message_fields)
	def put(self, message_id):
		args = post_parser.parse_args()
		message = Message.query.filter_by(id=message_id).first()
		if(not message):
				abort(404, message="message {} doesn't exist".format(message_id))
		if(not args.body):
			abort(404, message="El body es requerido no puede esta vacio")
		message.body = args.body
		message.privado = args.privado
		message.ticket_id = args.ticket_id
		message.from_user_id = args.from_user_id
		message.to_user_id   = args.to_user_id
		db.session.commit()
		return message,201

