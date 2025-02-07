# import jwt
import json
import hmac
import random
import hashlib
import datetime
from functools import wraps
from flaskapp.db_models import User
from flask import request, abort, current_app

with open('/etc/chatbot.json', 'r') as config_file:
# with open("C:/Users/User/Desktop/task/config.json", 'r') as config_file:
	config = json.load(config_file)

# handle login
def login_required(f):
	@wraps(f)
	def inner(*args, **kwargs):
		token = request.headers['x-access-token']

		if not token:
			abort(403)

		# read authorization prefix
		pre, token_ = token.split(' ')
		if pre == config.get('AUTHORIZATION_PREFIX'):
			token = token_
		else:
			abort(403)

		try:
			data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
			id = data['id']
			current_user = User.query.filter_by(id=id).first()
		except:
			abort(401)
		return f(current_user, *args, **kwargs)
	return inner


def logout_required(f):
	@wraps(f)
	def inner(*args, **kwargs):
		token = request.headers['x-access-token']
		if token and len(token) <= 32:
			abort(403)
		return f(*args, **kwargs)
	return inner


# generate a random 6 digit number used as otp
def generate_otp():
	return format(random.randint(0,999999), "06d")

# create a hmac with response data and otp
def create_hmac(data, secret, otp):
	data.update({'otp':otp})
	key = json.dumps(data, separators=(',', ':')).encode('utf-8')
	computed_hmac = hmac.new(secret.encode('utf-8'), key, hashlib.sha256).hexdigest()
	return computed_hmac

# verify hmac to ensure that user put the right otp from email
def verify_hmac(data, secret, otp, hmac_):
	# set timeout functionality
	createTime = datetime.datetime.fromisoformat(data['createTime'])
	timeout = createTime + datetime.timedelta(minutes=current_app.config['OTP_TIMEOUT'])
	currentTime = datetime.datetime.now(datetime.timezone.utc)

	if currentTime > timeout:
		return False

	# if not timeout than verify hmac
	data.update({'otp':otp})
	key = json.dumps(data, separators=(',', ':')).encode('utf-8')
	computed_hmac = hmac.new(secret.encode('utf-8'), key, hashlib.sha256).hexdigest()

	if computed_hmac == hmac_:
		return True
	else:
		return False
