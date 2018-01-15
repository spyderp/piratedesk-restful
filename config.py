import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI ='mysql://prueba:prueba@localhost/piratedesk2'
	SQLALCHEMY_TRACK_MODIFICATIONS = False