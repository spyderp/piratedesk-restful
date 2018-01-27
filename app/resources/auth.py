from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from app import db
from app.models import User, RevokedToken
from datetime import datetime

post_parser = reqparse.RequestParser()
post_parser.add_argument('username', location='json', required=True)
post_parser.add_argument('password', location='json',  required=True)
class Auth(Resource):
	def post(self):
		args = post_parser.parse_args()
		user = User.query.filter_by(username=args.username).filter_by(activo=1).first()
		if (user):
			if(user.check_password(args.password)):
				last = user.ultimo_acceso
				user.ultimo_acceso = datetime.utcnow
				db.session.commit()
				access_token = create_access_token(identity = args.username)
				refresh_token = create_refresh_token(identity = args.username)
				return {
					'user':{
						'id': user.id,
						'nombre': user.nombre,
						'apellido': user.apellido,
						'email': user.email,
						'ultimo_acceso': last,
						'puntaje': user.puntaje,
					},
					'access_token':access_token,
					'refresh_token':refresh_token
				}, 200
		abort(404, message="You username {} and/or password {} is incorrect, please try again".format(args.username, args.password))

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


class LogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
        	return {'message': 'Something went wrong'}, 500

class LogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500