# -*- coding: utf-8 -*-
from flask import render_template
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flask_jwt_extended import jwt_required
from app import db
from app.models import User, File, ForgotPassword
from app.commons import send_email, password_generator, token_generator, DateTimeLatinFormat
from time import time

post_parser = reqparse.RequestParser()
post_parser.add_argument('username', location='json', required=True, help='Usuario')
post_parser.add_argument('password', location='json', required=True, help='Contraseña')
post_parser.add_argument('nombre', location='json',  help='Nombre ')
post_parser.add_argument('apellido', location='json',  help='Apellido')
post_parser.add_argument('email', location='json',  help='Correo Electronico')
post_parser.add_argument('rol_id', location='json',  help='Rol')
put_parser = post_parser
put_parser.add_argument('activo', location='json',  help='Activo')
patch_parser = reqparse.RequestParser()
patch_parser.add_argument('email', location='json',  required=True, help='Correo Electronico')
patch_parser.add_argument('password', location='json',  help='Contraseña')

user_fields = {
	'id': fields.Integer,
	'username': fields.String,
	'nombre': fields.String,
	'apellido': fields.String,
	'email': fields.String,
	'activo': fields.String,
	'creado': DateTimeLatinFormat(),
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
		if(args.password):
			user.set_password(args.password)
		db.session.commit()
		return user,201

	def patch(self, user_id):
		args = patch_parser.parse_args()
		user = User.query.filter_by(id=user_id).first()
		if(not user):
				abort(404, message="User {} doesn't exist".format(user_id))
		user.email = args.email,
		if(args.password):
			user.set_password(args.password)
		db.session.commit()
		return 201

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
				send_email('[Piratedesk] Reset Your Password','ricardo.portillo@meduca.gob.pa',[user.email],text_body, html_body)
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
			send_email('[Piratedesk] new Your Password','ricardo.portillo@meduca.gob.pa',[user.email],text_body, html_body)
			return 201
		abort(404, message="token {} is incorrect".format(token))