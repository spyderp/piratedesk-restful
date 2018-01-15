files = db.Table('files',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('file_id', db.Integer, db.ForeignKey('file.id'), primary_key=True)
)
deparments = db.Table('deparments',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('deparment_id', db.Integer, db.ForeignKey('departmet.id'), primary_key=True)
)

messages = db.Table('messages',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('message_id', db.Integer, db.ForeignKey('message.id'), primary_key=True)
)