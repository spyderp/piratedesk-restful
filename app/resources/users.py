# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flask_jwt_extended import jwt_required
from app import db
from app.models import User, File
post_parser = reqparse.RequestParser()
post_parser.add_argument('username', location='json', required=True, help='Usuario')
post_parser.add_argument('password', location='json', required=True, help='Contraseña')
post_parser.add_argument('nombre', location='json',  help='Nombre ')
post_parser.add_argument('apellido', location='json',  help='Apellido')
post_parser.add_argument('email', location='json',  help='Correo Electronico')
post_parser.add_argument('rol_id', location='json',  help='Rol')
put_parser = post_parser
put_parser.add_argument('activo', location='json',  help='Activo')


user_fields = {
	'id': fields.Integer,
	'username': fields.String,
	'nombre': fields.String,
	'apellido': fields.String,
	'email': fields.String,
	'activo': fields.String,
	'creado': fields.DateTime(),
	'modificado': fields.DateTime(),
	'ultimo_acceso': fields.DateTime(),
	'puntaje': fields.Integer,
}
class Users(Resource):
	@jwt_required
	@marshal_with(user_fields)
	def get(self, user_id=None):
		if(not user_id):
			user = User.query.all()
		else:
			user = User.query.filter_by(id=user_id).first()
			if(not user):
				abort(404, message="User {} doesn't exist".format(user_id))
		return user
	@jwt_required
	@marshal_with(user_fields)
	def post(self):
		args = post_parser.parse_args()
		if(not args.username or  not args.password):
			abort(404, message="username and password required")
		user = User(
			username = args.username,
			nombre = args.nombre,
			apellido = args.apellido,
			email = args.email,
			rol_id = args.rol_id,
		)
		user.set_password(args.password)
		db.session.add(user)
		db.session.commit()
		return user,201

	@jwt_required
	@marshal_with(user_fields)
	def put(self, user_id):
		args = put_parser.parse_args()
		user = User.query.filter_by(id=user_id).first()
		if(not user):
				abort(404, message="User {} doesn't exist".format(user_id))
		if(not args.username):
			abort(404, message="username  required")
		user.username = args.username,
		user.nombre = args.nombre,
		user.apellido = args.apellido,
		user.email = args.email,
		user.activo =user.activo
		user.rol_id = args.rol_id
		if(args,password):
			user.set_password(args.password)
		db.session.commit()
		return user,201
