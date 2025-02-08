# Usage
You can ask whatever you want but the max answer token will be 500.
If we want to know realtime weather data, we must have mention the place.

> Conversational ai - Gemini
- [Ai model - gemini-2.0-flash](https://ai.google.dev/gemini-api/docs/quickstart?lang=python)
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

> Testing & Optimization
- pytest for test the backend


# API configuration
Generate a api key from [google aistudion](https://aistudio.google.com/prompts/new_chat).
Create the instance. `client = genai.Client(api_key=GENAI_API)`

```
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
```


# Deployment - GCP
- Nginx for reverse proxy, ssl
- gunicorn for serve the backend
- run the server in the background as service

Nginx configuration
```
server {
    server_name webwaymark.com www.webwaymark.com;
    include /etc/nginx/proxy_params;

    location / {
        root /home/username/conversational-ai/frontend/dist;
        try_files $uri /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:5000;
    }
}
```

Run the server as service
```
[Unit]
After=network.target

[Service]
WorkingDirectory=/home/username/conversational-ai
ExecStart=/home/username/conversational-ai/.env/bin/gunicorn -w 5 --bind localhost:5000 run:app
```