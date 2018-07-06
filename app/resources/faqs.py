# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, fields, marshal_with, abort, marshal
from flask_jwt_extended import jwt_required
from app import db
from app.models import Faq
from app.commons import roles_required, DateTimeLatinFormat

# Argumentos enviados por post o put
post_parser = reqparse.RequestParser()
post_parser.add_argument('title', location='json', required=True,)
post_parser.add_argument('content', location='json', required=True,)
post_parser.add_argument('orden', location='json', required=True,)
post_parser.add_argument('category_id', location='json', required=True,)


#data fields: datos a retornar
data_fields = {
	'id': fields.Integer,
	'title': fields.String,
	'content': fields.String,
	'orden': fields.Integer,
	'creado': DateTimeLatinFormat(),
	'modificado': DateTimeLatinFormat(),
	'category_id': fields.Integer,
}


class Faqs(Resource):
	@marshal_with(data_fields)
	def get(self, faq_id=None):
		if(not faq_id):
			result = Faq.query.order_by(Faq.orden).all()
		else:
			result = Faq.query.filter_by(id=faq_id).first()
			if(not result):
				abort(404, message="Faq {} doesn't exist".format(faq_id))
		return result

	@jwt_required
	@roles_required('administrador', 'agente')
	def delete(self, faq_id):
		result = Faq.query.filter_by(id=faq_id).first()
		if(not result):
				abort(404, message="Faq {} doesn't exist".format(faq_id))
		db.session.delete(result)
		db.session.commit()
		return '', 204

	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def post(self):
		args = post_parser.parse_args()
		result = Faq.query.filter_by(title=args.title).count()
		if(result>0):
			abort(404, message="{} ya existe".format(args.title))
		newData = Faq(
			title   = args.title,
			content = args.content,
			orden   = args.orden,
			category_id   = args.category_id,
		)
		db.session.add(newData)
		db.session.commit()
		return newData,201

	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def put(self, faq_id):
		args = post_parser.parse_args()
		result = Faq.query.filter_by(id=faq_id).first()
		if(not result):
			abort(404, message="Faq {} doesn't exist".format(faq_id))
		if(result.title != args.title):
			result2 = Faq.query.filter_by(title=args.title).count()
			if(result2>0):
				abort(404, message="{} ya existe".format(args.title))
		#Datos a Editar
		#result.direccion   = args.direccion
		result.title   = args.title
		result.content = args.content
		result.orden   = args.orden
		result.category_id   = args.category_id
		db.session.commit()
		return result,201