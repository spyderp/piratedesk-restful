# -*- coding: utf-8 -*-
from flask import render_template
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flask_jwt_extended import jwt_required
from app import db
from app.models import User, File, ForgotPassword, Department, Client
from app.commons import send_email, password_generator, token_generator, DateTimeLatinFormat, roles_required
from time import time
from config import Config

post_parser = reqparse.RequestParser()
post_parser.add_argument('username', location='json', required=True, help='Usuario')
post_parser.add_argument('password', location='json', required=True, help='Contraseña')
post_parser.add_argument('nombre', location='json',  help='Nombre ')
post_parser.add_argument('apellido', location='json',  help='Apellido')
post_parser.add_argument('email', location='json',  help='Correo Electronico')
post_parser.add_argument('rol_id', location='json',  help='Rol')
post_parser.add_argument('departments',location='json', action='append')
post_parser.add_argument('clients',location='json', action='append')
put_parser = post_parser
put_parser.add_argument('activo', location='json', type=bool, help='Activo')
patch_parser = reqparse.RequestParser()
patch_parser.add_argument('email', location='json',  required=True, help='Correo Electronico')
patch_parser.add_argument('password', location='json',  help='Contraseña')
get_parser = reqparse.RequestParser()
get_parser.add_argument('client', location='args', )
departments_field = {'id': fields.Integer,}
clients_field = {'id': fields.Integer,}
user_fields = {
	'id': fields.Integer,
	'username': fields.String,
	'nombre': fields.String,
	'apellido': fields.String,
	'email': fields.String,
	'activo': fields.Integer,
	'creado': DateTimeLatinFormat(),
	'modificado': DateTimeLatinFormat(),
	'ultimo_acceso': DateTimeLatinFormat(),
	'puntaje': fields.Integer,
	'departments':fields.Nested(departments_field),
	'clients':fields.Nested(clients_field)
}
class Users(Resource):
	@jwt_required
	@marshal_with(user_fields)
	@roles_required('administrador', 'agente')
	def get(self, user_id=None):
		args = get_parser.parse_args()
		if(not user_id):
			if(args.client):
				user = User.query.filter_by(rol_id=4).all()
			else:
				user = User.query.filter(User.rol_id != 4).filter(User.rol_id != 5).all()
		else:
			user = User.query.filter(User.rol_id != 4).filter(User.rol_id != 5).filter_by(id=user_id).first()
			if(not user):
				abort(404, message="User {} doesn't exist".format(user_id))
		return user
		
	@jwt_required
	@marshal_with(user_fields)
	@roles_required('administrador', 'agente')
	def post(self):
		args = post_parser.parse_args()
		if(not args.username or  not args.password):
			abort(404, message="username and password required")
		newData = User(
			username = args.username,
			nombre = args.nombre,
			apellido = args.apellido,
			email = args.email,
			rol_id = args.rol_id,
		)
		newData.set_password(args.password)
		if args.departments:
			for department_id in args.departments:
				f = Department.query.filter_by(id=department_id).first()
				newData.departments.append(f)
		if args.clients:		
			for client_id in args.clients:
				c = Client.query.filter_by(id=client_id).first()
				newData.clients.append(c)
		try:
			db.session.add(newData)
			db.session.commit()
			return newData,201
		except AssertionError as exception_message:
			abort(400, message='Error:{}'.format(exception_message))

	@jwt_required
	@marshal_with(user_fields)
	@roles_required('administrador', 'agente')
	def put(self, user_id):
		args = put_parser.parse_args()
		result = User.query.filter_by(id=user_id).first()
		if(not result or user_id==1):
				abort(404, message="User {} doesn't exist".format(user_id))
		if(not args.username):
			abort(404, message="username  required")
		result.username = args.username,
		result.nombre = args.nombre,
		result.apellido = args.apellido,
		result.email  = args.email,
		result.activo = args.activo
		result.rol_id = args.rol_id
		if args.departments:
			for row in result.departments:
				f = Department.query.filter_by(id=row.id).first()
				result.departments.remove(f)
			for department_id in args.departments:
				f = Department.query.filter_by(id=department_id).first()
				result.departments.append(f)
		if args.clients:
			for row in result.clients:
				f = Client.query.filter_by(id=row.id).first()
				result.clients.remove(f)
			for client_id in args.clients:
				c = Client.query.filter_by(id=client_id).first()
				result.clients.append(c)
		if(args.password):
			result.set_password(args.password)
		try:
			db.session.commit()
			return result,201
		except AssertionError as exception_message:
			abort(400, message='Error:{}'.format(exception_message))

	@jwt_required
	@roles_required('administrador', 'agente')
	def patch(self, user_id):
		args = patch_parser.parse_args()
		user = User.query.filter_by(id=user_id).first()
		if(not user or user_id==1):
				abort(404, message="User {} doesn't exist".format(user_id))
		user.email = args.email,
		if(args.password):
			user.set_password(args.password)
		try:
			db.session.commit()
			return user,201
		except AssertionError as exception_message:
			abort(400, message='Error:{}'.format(exception_message))

resetpost_parser = reqparse.RequestParser()
resetpost_parser.add_argument('email', location='json',  help='Correo Electronico')
class Reset_password_request(Resource):
	def post(self):
		args = resetpost_parser.parse_args()
		user = User.query.filter_by(email=args.email).first()
		if user:
			forgot = ForgotPassword.query.filter_by(user_id=user.id).filter_by(status=1).filter(ForgotPassword.expired<=time()).first()
			if not forgot:
				token = token_generator()
				f = ForgotPassword(
					token = token,
					password = password_generator(),
					expired = time() + (60*60),
					user_id = user.id 
				)
				db.session.add(f)
				db.session.commit()
				text_body  = render_template('email/reset_password.txt',user=user, token=token)
				html_body=render_template('email/reset_password.html',user=user, token=token)
				send_email('[{}] Reset Your Password'.format(Config.SITENAME),Config.MAILSYS,[user.email],text_body, html_body)
				return 201
		abort(404, message="email {} doesn't exist".format(args.email))

class  Reset_password(Resource):
	def get(self, token):
		forgot = ForgotPassword.query.filter_by(token=token).filter_by(status=1).filter(ForgotPassword.expired>=time()).first()
		if forgot:
			user = User.query.filter_by(id=forgot.user_id).first()
			forgot.status=0
			password = forgot.password
			user.set_password(password)
			db.session.commit()
			text_body  = render_template('email/new_password.txt',password=password)
			html_body=render_template('email/new_password.html',password=password)
			send_email('[{}}] new Your Password'.format(Config.SITENAME),Config.MAILSYS,[user.email],text_body, html_body)
			return 201
		abort(404, message="token {} is incorrect".format(token))