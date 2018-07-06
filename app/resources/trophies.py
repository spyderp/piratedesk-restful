# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, fields, marshal_with, abort, marshal
from flask_jwt_extended import jwt_required
from app import db
from app.models import Trophy
from app.commons import roles_required,DateTimeLatinFormat

# Argumentos enviados por post o put
post_parser = reqparse.RequestParser()
post_parser.add_argument(
	'descripcion', 
	location='json', required=True,
	help='Descripción',
)
post_parser.add_argument(
	'puntos', 
	location='json', required=True,
	help='Puntaje',
)

post_parser.add_argument(
	'file_id', 
	location='json', required=True,
)


#data fields: datos a retornar
data_fields = {
	'id': fields.Integer,
	'descripcion': fields.String,
	'puntos': fields.Integer,
	'creado': DateTimeLatinFormat(),
	'modificado': DateTimeLatinFormat(),
	'file_id': fields.Integer,

}


class Trophies(Resource):
	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def get(self, trophy_id=None):
		if(not trophy_id):
			result = Trophy.query.all()
		else:
			result = Trophy.query.filter_by(id=trophy_id).first()
			if(not result):
				abort(404, message="Trophy {} doesn't exist".format(trophy_id))
		return result

	@jwt_required
	@roles_required('administrador', 'agente')
	def delete(self, trophy_id):
		result = Trophy.query.filter_by(id=trophy_id).first()
		if(not result):
				abort(404, message="Trophy {} doesn't exist".format(trophy_id))
		db.session.delete(result)
		db.session.commit()
		return '', 204

	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def post(self):
		args = post_parser.parse_args()
		result = Trophy.query.filter(Trophy.puntos<=args.puntos).count()
		if(result>0):
			abort(404, message="El puntaje  {} es menor o igual a otro registrado".format(args.puntos))
		newData = Trophy(
			descripcion = args.descripcion,
			puntos      = args.puntos,
			file_id     = args.file_id
		)
		db.session.add(newData)
		db.session.commit()
		return newData,201

	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def put(self, trophy_id):
		args = post_parser.parse_args()
		result = Trophy.query.filter_by(id=trophy_id).first()
		if(not result):
				abort(404, message="Trophy {} doesn't exist".format(trophy_id))
		#Datos a Editar
		#result.direccion   = args.direccion
		result.descripcion = args.descripcion
		result.puntos      = args.puntos
		result.file_id     = args.file_id
		db.session.commit()
		return result,201