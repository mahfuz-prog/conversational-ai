import requests
from flask_cors import CORS
from google.genai import types
from flaskapp import db, client
from flaskapp.users.utils import login_required
from flaskapp.db_models import Conversation, Message
from flask import request, Blueprint, jsonify, abort, current_app

# create bluprint instance
chats = Blueprint('chats', __name__, url_prefix='/api')
CORS(chats)

sys_instruct = '''Your name is Neko. You have been implemented in a Chatbot Application.
	Analyze the sentiment of the user's input and answer accordingly'''

# API cal for get current weather data
def get_current_weather(location: str) -> str:
	weathe_api = current_app.config['WEATHER_API']
	url = f'http://api.weatherapi.com/v1/current.json?key={weathe_api}&q={location}'
	response = requests.get(url).text
	return response


# return model reply
def generate_model_response(history):
	# pass the history with current question, sys_instruct, and external api call functionality
	model = client.models.generate_content(
		model="gemini-2.0-flash",
		contents=history,
		config=types.GenerateContentConfig(
			max_output_tokens=500,
			temperature=0.3,
			system_instruction=sys_instruct,
			tools=[get_current_weather]
		)
	)

	return model.text


# public chat route
@chats.route('/', methods=['POST'])
def home():
	data = ''
	if request.method == 'POST':
		response = request.get_json()
		if 'history' not in response:
			# bad request
			abort(400)

		temp_history = response['history']
		history = []
		for i in temp_history:
			history.append({"role": i['role'], "parts":[{"text": i['text']}]})

		bot_reply = generate_model_response(history)
		if bot_reply:
			data = bot_reply

	return jsonify(data)


# loggeding user chat route
@chats.route('/chat/', methods=['POST'])
@login_required
def chat(current_user):
	data = {}
	if request.method == 'POST':
		response = request.get_json()
		if not response or 'message' not in response or 'conversationId' not in response:
			# bad request
			abort(400)
		
		message = str(response['message'])
		conversation_id = int(response['conversationId'])

		# load the conversation which is requested
		conversation = db.session.get(Conversation, conversation_id)

		# if the requested conversation dose not belong to current user
		# return a forbidden response
		if conversation.user_id != current_user.id:
			abort(403)


		# save user message to database
		message = Message(role='user', text=message, conversation_id=conversation_id)
		db.session.add(message)
		db.session.commit()

		# create history from db
		history = []
		messages_db = Message.query.filter_by(conversation_id=conversation_id).limit(10)
		for i in messages_db:
			history.append({"role": i.role, "parts":[{"text": i.text}]})


		# save bot reply to database
		bot_reply = generate_model_response(history)
		if bot_reply:
			message = Message(role='model', text=bot_reply, conversation_id=conversation_id)
			db.session.add(message)
			db.session.commit()

		data.update({'conversationId': conversation_id})
		data.update({'botReply': bot_reply})

	return jsonify(data)


# return a history of conversation id and thier first title
# for last 10 history
@chats.route('/history/')
@login_required
def history(current_user):
	data = []
	# filter all the converation of a user
	conversations = current_user.conversations
	if conversations:
		for conversation in conversations:
			# newly created conversation dosent have a message
			try:
				first_message = Message.query.filter_by(conversation_id=conversation.id).first().text
			except:
				first_message = 'Start Chating'
			data.append({'conversationId': conversation.id, 'title': first_message[0:15]})

	return jsonify(data)


@chats.route('/new-conversation/')
@login_required
def new_conversation(current_user):
	if len(current_user.conversations) >= 5:
		# too many request
		abort(429)

	# create a new converation
	conversation = Conversation(author=current_user)
	db.session.add(conversation)
	db.session.commit()

	return jsonify({'conversationId': conversation.id, 'title': 'Start Chating'})


@chats.route('/single-conversation/<int:id>')
@login_required
def single_conversation(current_user, id):
	data = []
	conversation = db.session.get(Conversation, id)

	# if the requested conversation dose not belong to current user
	# return a forbidden response
	if conversation.user_id != current_user.id:
		abort(403)

	# filter the messages from the conversation
	messages = Message.query.filter_by(conversation_id=id).all()

	# check if there is a conversation and messages in database and their author is current user
	if conversation and messages:
		for message in messages:
			data.append({'role': message.role, 'text': message.text})

	return jsonify(data)