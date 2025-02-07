> Conversational ai - Gemini
- [Ai modle - gemini-2.0-flash](https://ai.google.dev/gemini-api/docs/quickstart?lang=python)
- In conversational AI, the model is responsible for understanding natural language and generating relevant responses.
- Provides the AI with the context of the ongoing conversation.
- Limits the length of the response to 500 tokens
- For context conversation between user and model saved in to database


> Backend Development - Flask
- Blueprint for better management and use different part of this application as package
- User authentication (signup, login, email verication) implemented using JWT (JSON Web Tokens).
- Sqlite3 database with flask-sqlalchemy ORM(object relational mapper)
- Conversation history, User info are stored in database for personalize the experience

> Frontend Interface - VueJs
- Pages: home, signup, login, account, chat

> Integrations
- [weatherapi](https://www.weatherapi.com/). This is a free api to get current weather data
- If any user request for weather our model will automaticall call this api.
- user can interect our from chat page if logged in or homepage for logout user.
- user data will send to our backend server using post request.

> Deployment - GCP, Nginx
