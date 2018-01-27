# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flask_jwt_extended import jwt_required
from app import db
from app.models import Department
post_parser = reqparse.RequestParser()
post_parser.add_argument('descripcion', location='json', required=True, help='descripción')
post_parser.add_argument('user_id', location='json')
post_parser.add_argument('parent_id', location='json')

user_fields = {
		'id': fields.Integer,
		'username': fields.String,
		'nombre': fields.String,
		'apellido': fields.String,
		'email': fields.String,
}
child_fields = {
	'id': fields.Integer,
	'descripcion': fields.String,
}
department_fields = {
	'id': fields.Integer,
	'descripcion': fields.String,
	'children': fields.Nested(child_fields),
	'users': fields.Nested(user_fields),
}

class Departments(Resource):
	@jwt_required
	@marshal_with(department_fields)
	def get(self, department_id=None):
		if(not department_id):
			department = Department.query.all()
		else:
			department = Department.query.filter_by(id=department_id).first()
			if(not department):
				abort(404, message="Department {} doesn't exist".format(department_id))
		return department
	@jwt_required
	def delete(self, department_id):
		department = Department.query.filter_by(id=department_id).first()
		if(not department):
				abort(404, message="Department {} doesn't exist".format(department_id))
		db.session.delete(department)
		db.session.commit()
		return '', 204
	@jwt_required
	@marshal_with(department_fields)
	def post(self):
		args = post_parser.parse_args()
		department = Department(
			descripcion	= args.descripcion,
			parent_id   = args.parent_id,
			user_id 	= args.user_id,
		)
		db.session.add(department)
		db.session.commit()
		return department,201
	@jwt_required
	@marshal_with(department_fields)
	def put(self, department_id):
		args = post_parser.parse_args()
		department = Department.query.filter_by(id=department_id).first()
		if(not department):
				abort(404, message="Department {} doesn't exist".format(department_id))
		if(not args.nombre):
			abort(404, message="El nombre es requerido no puede esta vacio")
		department.descripcion = args.descripcion,
		department.parent_id   = args.parent_id,
		department.user_id 	   = args.user_id,
		db.session.commit()
		return department,201