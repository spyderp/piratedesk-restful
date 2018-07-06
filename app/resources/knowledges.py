# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, fields, marshal_with, abort, marshal
from flask_jwt_extended import jwt_required
from app import db
from app.models import Knowledge
from app.commons import roles_required

# Argumentos enviados por post o put
post_parser = reqparse.RequestParser()
post_parser.add_argument('title', location='json', required=True,)
post_parser.add_argument('content', location='json', required=True,)
post_parser.add_argument('keys', location='json', required=True,)
post_parser.add_argument('department_id', location='json', required=True,)

# Argumentos enviados por GET
get_parser = reqparse.RequestParser()
get_parser.add_argument('find', location='args', help='for find')

# Argumentos enviados por PATCH
patch_parser = reqparse.RequestParser()
patch_parser.add_argument('rating', location='json')
patch_parser.add_argument('access', location='json')

#data fields: datos a retornar
data_fields = {
	'id': fields.Integer,
	'title': fields.String,
	'content': fields.String,
	'keys': fields.String,
	'creado': fields.DateTime(),
	'modificado': fields.DateTime(),
	'rating': fields.Integer,
	'access': fields.Integer,
	'department_id': fields.Integer,
}


class Knowledges(Resource):
	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def get(self, knowledge_id=None):
		if(not knowledge_id):
			result = Knowledge.query.all()
		else:
			result = Knowledge.query.filter_by(id=knowledge_id).order_by(Knowledge.creado) .first()
			if(not result):
				abort(404, message="User {} doesn't exist".format(knowledge_id))
		return result

	@jwt_required
	@roles_required('administrador', 'agente')
	def delete(self, knowledge_id):
		result = Knowledge.query.filter_by(id=knowledge_id).first()
		if(not result):
				abort(404, message="Knowledge {} doesn't exist".format(knowledge_id))
		db.session.delete(result)
		db.session.commit()
		return '', 204

	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def post(self):
		args = post_parser.parse_args()
		newData = Knowledge(
			title = args.title,
			content = args.content,
			keys = args.keys,
			department_id = args.department_id,
		)
		db.session.add(newData)
		db.session.commit()
		return newData,201

	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def put(self, knowledge_id):
		args = post_parser.parse_args()
		result = Knowledge.query.filter_by(id=knowledge_id).first()
		if(not result):
				abort(404, message="Knowledge {} doesn't exist".format(knowledge_id))
		if(not args.title):
			abort(404, message="El nombre es requerido no puede esta vacio")
		#Datos a Editar
		#result.direccion   = args.direccion
		result.title = args.title,
		result.content = args.content,
		result.keys = args.keys,
		result.department_id = args.department_id,
		db.session.commit()
		return result,201

	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def patch(self, knowledge_id):
		args = patch_parser.parse_args()
		result = Knowledge.query.filter_by(id=knowledge_id).first()
		if(not result):
				abort(404, message="User {} doesn't exist".format(knowledge_id))
		if(args.rating):
			result.rating = args.rating
		if(args.access):
			result.access = args.access
		try:
			db.session.commit()
			return result,201
		except AssertionError as exception_message:
			abort(400, message='Error:{}'.format(exception_message))
