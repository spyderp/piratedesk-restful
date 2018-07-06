# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, fields, marshal_with, abort, marshal
from flask_jwt_extended import jwt_required
from app import db
from app.models import Festive
from app.commons import roles_required, DateTimeLatinFormat

# Argumentos enviados por post o put
post_parser = reqparse.RequestParser()
post_parser.add_argument('descripcion', location='json', required=True,)
post_parser.add_argument('fecha', location='json', required=True,)

get_parser = reqparse.RequestParser()
get_parser.add_argument('type', location='args', help='formato respuesta')
#data fields: datos a retornar
data_fields = {
	'id': fields.Integer,
	'descripcion': fields.String,
	'fecha': fields.String,
}


class Festives(Resource):
	@jwt_required
	@roles_required('administrador', 'agente')
	def get(self, festive_id=None):
		args = get_parser.parse_args()
		if(not festive_id):
			result = Festive.query.all()
		else:
			result = Festive.query.filter_by(id=festive_id).first()
			if(not result):
				abort(404, message="Festive {} doesn't exist".format(festive_id))
		if(args.type=='list'):
			data = []
			for row in result:
				data.append({'id':row.id, 'text':row.descripcion})
		return marshal(result,data_fields)  if not args.type  else data

	@jwt_required
	@roles_required('administrador', 'agente')
	def delete(self, festive_id):
		result = Festive.query.filter_by(id=festive_id).first()
		if(not result):
				abort(404, message="Festive {} doesn't exist".format(festive_id))
		db.session.delete(result)
		db.session.commit()
		return '', 204

	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def post(self):
		args = post_parser.parse_args()
		newData = Festive(
			descripcion = args.descripcion,
			fecha = args.fecha,
		)
		db.session.add(newData)
		db.session.commit()
		return newData,201

	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def put(self, festive_id):
		args = post_parser.parse_args()
		result = Festive.query.filter_by(id=festive_id).first()
		if(not result):
				abort(404, message="Festive {} doesn't exist".format(festive_id))
		#Datos a Editar
		#result.direccion   = args.direccion
		result.descripcion = args.descripcion
		result.fecha = args.fecha
		db.session.commit()
		return result,201