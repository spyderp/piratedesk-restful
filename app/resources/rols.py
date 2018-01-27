# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort
from flask_jwt_extended import jwt_required
from app import db
from app.models import Rol

rol_fields = {
	'id': fields.Integer,
	'descripcion': fields.String,
	'privilege': fields.String,
}

class Rols(Resource):
	@jwt_required
	@marshal_with(rol_fields)
	def get(self, rol_id=None):
		if(not rol_id):
			rol = Rol.query.all()
		else:
			rol = Rol.query.filter_by(id=rol_id).first()
			if(not rol):
				abort(404, message="Rol {} doesn't exist".format(rol_id))
		return rol