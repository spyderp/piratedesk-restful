# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, fields, marshal_with, abort, marshal
from flask_jwt_extended import jwt_required
from app import db
from app.models import Department
from app.commons import roles_required

post_parser = reqparse.RequestParser()
post_parser.add_argument('descripcion', location='json', required=True, help='descripción')
post_parser.add_argument('user_id', location='json')
post_parser.add_argument('parent_id', location='json')

get_parser = reqparse.RequestParser()
get_parser.add_argument('type', location='args', help='formato respuesta')

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
	def get(self, department_id=None):
		args = get_parser.parse_args()
		if(not department_id):
			department = Department.query.all()
		else:
			department = Department.query.filter_by(id=department_id).first()
			if(not department):
				abort(404, message="Department {} doesn't exist".format(department_id))
		if(args.type=='list'):
			data = []
			for row in department:
				data.append({'id':row.id, 'text':row.descripcion})
		return marshal(department,department_fields)  if not args.type  else data
	
	@jwt_required
	@roles_required('administrador', 'agente')
	def delete(self, department_id):
		department = Department.query.filter_by(id=department_id).first()
		if(not department):
				abort(404, message="Department {} doesn't exist".format(department_id))
		department2 = Department.query.filter_by(parent_id=department_id).first()
		if department2:
			abort(404, message="You cannot delete the department with the id: {} because you have a child. ".format(department_id))
		db.session.delete(department)
		db.session.commit()
		return '', 204

	@jwt_required
	@roles_required('administrador', 'agente')
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
	@roles_required('administrador', 'agente')
	@marshal_with(department_fields)
	def put(self, department_id):
		args = post_parser.parse_args()
		department = Department.query.filter_by(id=department_id).first()
		if(not department):
				abort(404, message="Department {} doesn't exist".format(department_id))
		if(not args.descripcion):
			abort(404, message="El nombre es requerido no puede esta vacio")
		department.descripcion = args.descripcion
		department.parent_id   = args.parent_id
		department.user_id 	   = args.user_id
		db.session.commit()
		return department,201