import json

with open('/etc/chatbot.json', 'r') as config_file:
# with open("C:/Users/User/Desktop/task/config.json", 'r') as config_file:
	conf = json.load(config_file)

class Config():
	SECRET_KEY = conf.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = conf.get('SQLALCHEMY_DATABASE_URI')
	JWT_TIMEOUT = 100		# In minutes
	OTP_TIMEOUT = 2		# In minutes
	AUTHORIZATION_PREFIX = conf.get('AUTHORIZATION_PREFIX')

	# MAIL_SERVER configuration
	MAIL_SERVER = conf.get('MAIL_SERVER')
	MAIL_PORT = 465
	MAIL_USERNAME = conf.get('MAIL_USERNAME')	#email
	MAIL_PASSWORD = conf.get('MAIL_PASSWORD')	#app password
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True

	GENAI_API = conf.get('GENAI_API')
	WEATHER_API = conf.get('WEATHER_API')