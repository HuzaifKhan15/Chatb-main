from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)

# Load responses from a JSON file
def load_responses():
    try:
        with open('responses.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "greeting": ["Hello! How can I help you today?", "Hi there! What can I do for you?", "Welcome! How may I assist you?"],
            "help": ["I'm here to help. What do you need?", "How can I assist you today?", "What can I help you with?"],
            "default": ["I understand. Could you tell me more?", "That's interesting. Please continue.", "I'm listening. What else would you like to share?"]
        }

responses = load_responses()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').lower()
    
    # Simple response logic
    if any(word in user_message for word in ['hi', 'hello', 'hey']):
        response = random.choice(responses['greeting'])
    elif any(word in user_message for word in ['help', 'assist', 'support']):
        response = random.choice(responses['help'])
    else:
        response = random.choice(responses['default'])
    
    return jsonify({
        'message': response,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000) 