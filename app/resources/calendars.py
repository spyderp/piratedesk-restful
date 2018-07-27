# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, fields, marshal_with, abort, marshal
from flask_jwt_extended import jwt_required
from app import db
from app.models import Calendar, Festive
from app.commons import roles_required

# Argumentos enviados por post o put
post_parser = reqparse.RequestParser()
post_parser.add_argument('descripcion', location='json', required=True,)
post_parser.add_argument('dias', location='json')
post_parser.add_argument('hora_inicio', location='json')
post_parser.add_argument('hora_final', location='json')
post_parser.add_argument('fulltime', type=int,location='json')
post_parser.add_argument('festives',location='json', action='append')

# Argumentos enviados por GET
get_parser = reqparse.RequestParser()
get_parser.add_argument('type', location='args', help='formato respuesta')

#data fields: datos a retornar
festive_field = {'id': fields.Integer,}
data_fields = {
	'id': fields.Integer,
	'descripcion': fields.String,
	'dias': fields.String,
	'hora_inicio': fields.String,
	'hora_final': fields.String,
	'fulltime': fields.Integer,
	'festives':fields.Nested(festive_field)
}


class Calendars(Resource):
	@jwt_required
	@roles_required('administrador', 'agente')
	def get(self, calendar_id=None):
		args = get_parser.parse_args()
		if(not calendar_id):
			result = Calendar.query.all()
		else:
			result = Calendar.query.filter_by(id=calendar_id).first()
			if(not result):
				abort(404, message="Calendar {} doesn't exist".format(calendar_id))
		if(args.type=='list'):
			data = []
			for row in result:
				data.append({'id':row.id, 'text':row.descripcion})
		return marshal(result,data_fields)  if not args.type  else data

	@jwt_required
	@roles_required('administrador')
	def delete(self, calendar_id):
		result = Calendar.query.filter_by(id=calendar_id).first()
		if(not result):
				abort(404, message="Calendar {} doesn't exist".format(calendar_id))
		db.session.delete(result)
		db.session.commit()
		return '', 204

	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def post(self):
		args = post_parser.parse_args()
		newData = Calendar(
			descripcion = args.descripcion,
			dias = args.dias,
			hora_inicio = args.hora_inicio,
			hora_final = args.hora_final,
			fulltime = args.fulltime,
		)
		for festive_id in args.festives:
			f = Festive.query.filter_by(id=festive_id).first()
			newData.festives.append(f)
		db.session.add(newData)
		db.session.commit()
		return newData,201

	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def put(self, calendar_id):
		args = post_parser.parse_args()
		result = Calendar.query.filter_by(id=calendar_id).first()
		if(not result):
				abort(404, message="Calendar {} doesn't exist".format(calendar_id))
		#Datos a Editar
		#result.direccion   = args.direccion
		result.descripcion = args.descripcion
		result.dias = args.dias
		result.hora_inicio = args.hora_inicio
		result.hora_final = args.hora_final
		result.fulltime = args.fulltime
		for row in result.festives:
			f = Festive.query.filter_by(id=row.id).first()
			result.festives.remove(f)
		for festive_id in args.festives:
			f = Festive.query.filter_by(id=festive_id).first()
			result.festives.append(f)
		db.session.commit()
		return result,201