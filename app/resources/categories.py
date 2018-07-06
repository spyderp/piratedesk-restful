# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, fields, marshal_with, abort, marshal
from flask_jwt_extended import jwt_required
from app import db
from app.models import Category
from app.commons import roles_required

# Argumentos enviados por post o put
post_parser = reqparse.RequestParser()
post_parser.add_argument('name', location='json', required=True,)
post_parser.add_argument('descripcion', location='json', required=True,)


#data fields: datos a retornar
data_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'descripcion': fields.String,
}


class Categories(Resource):
	@marshal_with(data_fields)
	def get(self, category_id=None):
		if(not category_id):
			result = Category.query.order_by(Category.name).all()
		else:
			result = Category.query.filter_by(id=category_id).first()
			if(not result):
				abort(404, message="Category {} doesn't exist".format(category_id))
		return result

	@jwt_required
	@roles_required('administrador', 'agente')
	def delete(self, category_id):
		result = Category.query.filter_by(id=category_id).first()
		if(not result):
				abort(404, message="Category {} doesn't exist".format(category_id))
		db.session.delete(result)
		db.session.commit()
		return '', 204

	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def post(self):
		args = post_parser.parse_args()
		result = Category.query.filter_by(name=args.name).count()
		if(result>0):
			abort(404, message="{} ya existe".format(args.name))
		newData = Category(
			name   = args.name,
			descripcion = args.descripcion,
		)
		db.session.add(newData)
		db.session.commit()
		return newData,201

	@jwt_required
	@roles_required('administrador', 'agente')
	@marshal_with(data_fields)
	def put(self, category_id):
		args = post_parser.parse_args()
		result = Category.query.filter_by(id=category_id).first()
		if(not result):
			abort(404, message="Category {} doesn't exist".format(category_id))
		if(result.name != args.name):
			result2 = Category.query.filter_by(name=args.name).count()
			if(result2>0):
				abort(404, message="{} ya existe".format(args.name))
		#Datos a Editar
		#result.direccion   = args.direccion
		result.name   = args.name
		result.descripcion = args.descripcion
		db.session.commit()
		return result,201