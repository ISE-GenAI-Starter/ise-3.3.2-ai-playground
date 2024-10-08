import json
import time
import traceback
import os
import logging

from flask import Flask, render_template, request

from ai import get_chat_reply, PASSWORDS

# Load .env file for local development
from dotenv import load_dotenv
load_dotenv()

# Simple auth password just to prevent rampant abuse
AUTH_PASSWORD = os.environ.get('AUTH_PASSWORD')

# Simple rate limiting to prevent rampant abuse
TIMEOUT_SEC = 2

app = Flask(__name__)

simple_rate_limiting = dict()
def is_rate_limited(ip):
    if ip in simple_rate_limiting:
        if simple_rate_limiting[ip] + TIMEOUT_SEC < time.time():
            return False
        else:
            return True
    else:
        simple_rate_limiting[ip] = time.time()
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if is_rate_limited(request.remote_addr):
        return json.dumps({"status": "error", "errors": ["Too many requests! Try again in a few seconds."]})

    data = request.get_json()
    try:
        password = data.get('password')
    except KeyError:
        return json.dumps({"status": "error", "errors": ["Password is required."]})

    if password != AUTH_PASSWORD:
        return json.dumps({"status": "error", "errors": ["Password is incorrect."]})

    return json.dumps({"status": "success"})

@app.route('/check', methods=['POST'])
def check():
    if is_rate_limited(request.remote_addr):
        return json.dumps({"status": "error", "errors": ["Too many requests! Try again in a few seconds."]})

    data = request.get_json()
    errors = []
    try:
        auth = data.get('auth')
        if auth != AUTH_PASSWORD:
            return json.dumps({"status": "error", "errors": ["Incorrect auth! Login and try again."]})
    except ValueError:
        return json.dumps({"status": "error", "errors": ["Must provide auth"]})

    try:
        level = int(data.get('level'))
    except ValueError:
        errors.append('level must be an integer.')
    except KeyError:
        errors.append('level is required.')
    try:
        secret = data.get('secret')
    except KeyError:
        errors.append('secret is required.')
    
    if errors:
        return json.dumps({"status": "error", "errors": errors})
    else:
        return json.dumps({"status": "success", "secret": "true" if secret == PASSWORDS[level - 1] else "false"})


@app.route('/ai', methods=['POST'])
def ai():    
    if is_rate_limited(request.remote_addr):
        return json.dumps({"status": "error", "errors": ["Too many requests! Try again in a few seconds."]})

    data = request.get_json()
    errors = []
    try:
        auth = data.get('auth')
        if auth != AUTH_PASSWORD:
            return json.dumps({"status": "error", "errors": ["Incorrect auth! Login and try again."]})
    except ValueError:
        return json.dumps({"status": "error", "errors": ["Must provide auth"]})

    try:
        level = int(data.get('level'))
    except ValueError:
        errors.append('level must be an integer.')
    except KeyError:
        errors.append('level is required.')
    try:
        userPrompt = data.get('userPrompt')
    except KeyError:
        errors.append('userPrompt is required.')

    if not errors:
        try:
            chatReply = get_chat_reply(level, userPrompt)
        except:
            err = "There was an error getting a reply from the chatbot, please try again."
            logging.exception(err)
            errors.append(err)
        
    if errors:
        return json.dumps({"status": "error", "errors": errors})
    else:
        return json.dumps({"status": "success", "reply": chatReply})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))