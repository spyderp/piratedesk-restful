# -*- coding: utf-8 -*-
from json import dumps

def to_json(model):
	""" Returns a JSON representation of an SQLAlchemy-backed object.
	"""
	json = {}
	json['fields'] = {}

	for col in model._sa_class_manager.mapper.mapped_table.columns:
		json['fields'][col.name] = getattr(model, col.name)

	return dumps([json])