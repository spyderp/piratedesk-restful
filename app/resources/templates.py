# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, fields, marshal_with, abort, marshal
from flask_jwt_extended import jwt_required
from app import db
from app.models import Template
from app.commons import roles_required, DateTimeLatinFormat

# Argumentos enviados por post o put
post_parser = reqparse.RequestParser()
post_parser.add_argument('descripcion', location='json', required=True)
post_parser.add_argument('body', location='json', required=True)

# Argumentos enviados por GET
get_parser = reqparse.RequestParser()
get_parser.add_argument('type', location='args', help='formato respuesta')

#data fields: datos a retornar
data_fields = {
	'id': fields.Integer,
	'descripcion': fields.String,
	'body': fields.String,
	'creado': DateTimeLatinFormat(),
	'modificado': DateTimeLatinFormat(),
}


class Templates(Resource):
	@jwt_required
	@roles_required(['administrador', 'agente', 'supervisor'])
	@marshal_with(data_fields)
	def get(self, template_id=None):
		if(not template_id):
			result = Template.query.all()
		else:
			result = Template.query.filter_by(id=template_id).first()
			if(not result):
				abort(404, message="Template {} doesn't exist".format(template_id))
		return result

	@jwt_required
	@roles_required(['administrador', 'agente'])
	def delete(self, template_id):
		result = Template.query.filter_by(id=template_id).first()
		if(not result):
				abort(404, message="Template {} doesn't exist".format(template_id))
		db.session.delete(result)
		db.session.commit()
		return '', 204

	@jwt_required
	@roles_required(['administrador', 'agente'])
	@marshal_with(data_fields)
	def post(self):
		args = post_parser.parse_args()
		result = Template.query.filter_by(descripcion=args.descripcion).count()
		if(result>0):
			abort(404, message="{} ya existe".format(args.descripcion))
		newData = Template(
			descripcion = args.descripcion,
			body        = args.body
		)
		db.session.add(newData)
		db.session.commit()
		return newData,201

	@jwt_required
	@roles_required(['administrador', 'agente'])
	@marshal_with(data_fields)
	def put(self, template_id):
		args = post_parser.parse_args()
		result = Template.query.filter_by(id=template_id).first()
		if(not result):
			abort(404, message="Template {} doesn't exist".format(template_id))
		if(result.descripcion != args.descripcion):
			result2 = Template.query.filter_by(descripcion=args.descripcion).count()
			if(result2>0):
				abort(404, message="{} ya existe".format(args.descripcion))
		#Datos a Editar
		result.descripcion = args.descripcion
		result.body = args.body
		db.session.commit()
		return result,201