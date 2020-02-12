# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, fields, marshal_with, abort, marshal
from flask_jwt_extended import jwt_required
from app import db
from app.models import Priority
from app.commons import roles_required

# Argumentos enviados por post o put
post_parser = reqparse.RequestParser()
post_parser.add_argument(
	'descripcion', 
	location='json', required=True,
)
post_parser.add_argument(
	'respuesta', 
	location='json', required=True,
)
post_parser.add_argument(
	'resuelto', 
	location='json', required=True,
)
post_parser.add_argument(
	'escalable', 
	 type=int,
	location='json'
)
get_parser = reqparse.RequestParser()
get_parser.add_argument('type', location='args', help='formato respuesta')
#data fields: datos a retornar
data_fields = {
	'id': fields.Integer,
	'descripcion': fields.String,
	'respuesta': fields.Integer,
	'resuelto': fields.Integer,
	'escalable': fields.Boolean,
}


class Priorities(Resource):
	@jwt_required
	@roles_required(['administrador', 'agente', 'supervisor'])
	def get(self, priority_id=None):
		args = get_parser.parse_args()
		if(not priority_id):
			result = Priority.query.all()
		else:
			result = Priority.query.filter_by(id=priority_id).first()
			if(not result):
				abort(404, message="Priority {} doesn't exist".format(priority_id))
		if(args.type=='list'):
			data = []
			for row in result:
				data.append({'id':row.id, 'text':row.descripcion})
		return marshal(result,data_fields)  if not args.type  else data

	@jwt_required
	@roles_required(['administrador', 'agente'])
	def delete(self, priority_id):
		result = Priority.query.filter_by(id=priority_id).first()
		if(not result):
				abort(404, message="Priority {} doesn't exist".format(priority_id))
		db.session.delete(result)
		db.session.commit()
		return '', 204

	@jwt_required
	@roles_required(['administrador', 'agente'])
	@marshal_with(data_fields)
	def post(self):
		args = post_parser.parse_args()
		newData = Priority(
			descripcion = args.descripcion,
			respuesta = args.respuesta,
			resuelto = args.resuelto,
			escalable = args.escalable,
		)
		db.session.add(newData)
		db.session.commit()
		return newData,201

	@jwt_required
	@roles_required(['administrador', 'agente'])
	@marshal_with(data_fields)
	def put(self, priority_id):
		args = post_parser.parse_args()
		result = Priority.query.filter_by(id=priority_id).first()
		if(not result):
				abort(404, message="Priority {} doesn't exist".format(priority_id))
		#Datos a Editar
		result.descripcion = args.descripcion
		result.respuesta = args.respuesta
		result.resuelto = args.resuelto
		result.escalable = args.escalable
		db.session.commit()
		return result,201