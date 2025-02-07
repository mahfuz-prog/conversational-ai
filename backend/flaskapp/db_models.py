from flaskapp import db
from datetime import datetime

# user model for user information
class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), unique=True, nullable=False)
	email = db.Column(db.String(30), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	# One-to-Many relationship: A user can have multiple conversations
	conversations = db.relationship('Conversation', backref='author', lazy=True)

	# username check while creating account
	@staticmethod
	def check_name(name):
		user = User.query.filter_by(username=name.lower().replace(' ', '-')).first()
		if user:
			return user
		return False

	# email check while creating account
	@staticmethod
	def check_email(email):
		user = User.query.filter_by(email=email).first()
		if user:
			return user
		return False

	def __repr__(self):
		return f'username: {self.username} | email: {self.email}'


# Represents a conversation between a user and the chatbot
class Conversation(db.Model):
	__tablename__ = 'conversation'
	id = db.Column(db.Integer, primary_key=True)

	# Foreign key to associate a conversation with a user
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	# One-to-Many relationship: A conversation can have multiple messages
	messages = db.relationship("Message", back_populates="conversation")

	def __repr__(self):
		return f'id: {self.id}'


# Represents individual messages within a conversation
class Message(db.Model):
	__tablename__ = 'message'
	id = db.Column(db.Integer, primary_key=True)
	role = db.Column(db.String, nullable=False)
	text = db.Column(db.String, nullable=False)

	# Foreign key to associate a message with a conversation
	conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))

	 # Relationship back to Conversation
	conversation = db.relationship("Conversation", back_populates="messages")

	def __repr__(self):
		return f'id: {self.id} | role: {self.role} | text: {self.text[0:25]}'