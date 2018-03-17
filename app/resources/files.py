from flask import send_from_directory, request
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flask_jwt_extended import (jwt_required,)
from app import app, db
from app.models import File
import werkzeug

#post_parser = reqparse.RequestParser()
#post_parser.add_argument('file', location='file',type=werkzeug.datastructures.FileStorage ,required=True, help='Archivo')
file_fields = {
	'id': fields.Integer,
	'filename': fields.String,
	'size': fields.Integer,
	'type': fields.String,
	'creado': fields.String,
}

class Files(Resource):
	@jwt_required
	def get(self, filename):
		return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
	
	@jwt_required
	@marshal_with(file_fields)
	def post(self):
		file= request.files['file']
		f = File()
		f.set_file(file)
		db.session.add(f)
		db.session.commit()
		return f,201

