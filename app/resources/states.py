# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, fields, marshal_with, abort, marshal
from flask_jwt_extended import jwt_required
from app import db
from app.models import State
from app.commons import roles_required

# Argumentos enviados por post o put
post_parser = reqparse.RequestParser()
post_parser.add_argument('descripcion', location='json', required=True,)

#data fields: datos a retornar
data_fields = {
	'id': fields.Integer,
	'descripcion': fields.String,
}


class States(Resource):
	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def get(self, state_id=None):
		if(not state_id):
			result = State.query.all()
		else:
			result = State.query.filter_by(id=state_id).first()
			if(not result):
				abort(404, message="State {} doesn't exist".format(state_id))
		return result

	@jwt_required
	@roles_required('administrador', 'agente')
	def delete(self, state_id):
		result = State.query.filter_by(id=state_id).first()
		if(not result):
				abort(404, message="State {} doesn't exist".format(state_id))
		db.session.delete(result)
		db.session.commit()
		return '', 204

	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def post(self):
		args = post_parser.parse_args()
		newData = State(
			descripcion = args.descripcion,
		)
		db.session.add(newData)
		db.session.commit()
		return newData,201

	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def put(self, state_id):
		args = post_parser.parse_args()
		result = State.query.filter_by(id=state_id).first()
		if(not result):
				abort(404, message="State {} doesn't exist".format(state_id))
		#Datos a Editar
		result.descripcion = args.descripcion
		db.session.commit()
		return result,201