import os
import streamlit as st
import random
import re
import json
from datetime import datetime
from dotenv import load_dotenv
from resources import CRISIS_RESOURCES, COPING_STRATEGIES, SELF_CARE_REMINDERS, WARNING_SIGNS
from earkick_responses import EARKICK_RESPONSES

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="Vibe Check Bot",
    page_icon="✨",
    layout="wide"
)

# Load API key from .env file (kept for future use)
load_dotenv()

# Load training data
def load_training_data():
    try:
        with open('trained_chatbot_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)['training_data']
    except FileNotFoundError:
        st.error("Training data not found. Please run train_chatbot.py first.")
        return []

# Initialize training data
training_data = load_training_data()

# Load responses from earkick_responses.py
def load_earkick_responses():
    try:
        from earkick_responses import EARKICK_RESPONSES
        return EARKICK_RESPONSES
    except ImportError:
        st.error("Could not load specialized responses. Using default responses.")
        return {}

# Load Earkick responses
earkick_responses = load_earkick_responses()

# Function to check for crisis keywords
def check_for_crisis_keywords(text):
    text = text.lower()
    crisis_keywords = [
        "suicide", "kill myself", "end my life", "hurt myself", "harm myself",
        "don't want to live", "want to die", "better off dead", "no point in living",
        "i don't want to be here anymore", "i wish i could disappear"
    ]
    
    for keyword in crisis_keywords:
        if keyword in text:
            return True, "self_harm"
    return False, None

# Function to detect issues
def detect_issue(text):
    text = text.lower()
    
    depression_keywords = ["depress", "sad", "empty", "hopeless"]
    anxiety_keywords = ["anxi", "worry", "stress", "panic"]
    
    if any(keyword in text for keyword in depression_keywords):
        return "depression"
    elif any(keyword in text for keyword in anxiety_keywords):
        return "anxiety"
    return "general"

# Function to find the most appropriate response from training data
def get_trained_response(user_input, conversation_type=None):
    user_input = user_input.lower()
    
    # First check for crisis keywords
    is_crisis, crisis_type = check_for_crisis_keywords(user_input)
    if is_crisis:
        crisis_responses = [item for item in training_data if item['type'] == 'warning_sign']
        if crisis_responses:
            return random.choice(crisis_responses)['response']
    
    # Then check conversation type
    if conversation_type:
        type_responses = [item for item in training_data if item['type'] == conversation_type]
        if type_responses:
            return random.choice(type_responses)['response']
    
    # Check for specific issues
    issue = detect_issue(user_input)
    if issue != 'general':
        # First check if we have specialized Earkick responses for this issue
        if issue in earkick_responses:
            return random.choice(earkick_responses[issue])
        
        # Then check training data
        issue_responses = [item for item in training_data if item.get('issue') == issue]
        if issue_responses:
            return random.choice(issue_responses)['response']
    
    # Default to a general response
    general_responses = [
        "I hear you. Would you like to tell me more about that?",
        "That sounds challenging. How are you feeling about it?",
        "I'm here to listen. What would be most helpful for you right now?",
        "Thank you for sharing that with me. Would you like to explore this further?",
        "I understand this is important to you. How can I best support you?",
        "That's a lot to deal with. What aspect is most difficult for you right now?",
        "I appreciate you opening up about this. What would help you feel more supported?",
        "It sounds like you're going through a tough time. What helps you cope when things get difficult?",
        "I'm here to support you through this. What would be a small step toward feeling better?",
        "Your feelings make complete sense given what you're experiencing. How can I help?"
    ]
    return random.choice(general_responses)

# Custom CSS
    st.markdown("""
    <style>
    /* Main theme colors and fonts */
    :root {
        --background-color: #1a1a1a;
        --text-color: #ffffff;
        --accent-color: #ff7b7b;
        --secondary-color: #2d2d2d;
    }
    
    /* Global styles */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    /* Header styles */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        color: var(--accent-color);
        font-size: 2.5rem;
        font-weight: bold;
    }
    
    .sub-header {
        text-align: center;
        color: #a8a8a8;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Chat container */
    .chat-container {
        max-width: 800px;
            margin: 0 auto;
            padding: 20px;
    }
    
    /* Message bubbles */
    .user-message {
        background-color: var(--accent-color);
        color: white;
        padding: 12px 20px;
        border-radius: 20px;
        margin: 10px 0;
        max-width: 70%;
        float: right;
        clear: both;
    }
    
    .bot-message {
        background-color: var(--secondary-color);
        color: white;
        padding: 12px 20px;
            border-radius: 20px;
        margin: 10px 0;
        max-width: 70%;
        float: left;
        clear: both;
    }
    
    /* Input box */
    .stTextInput input {
        background-color: var(--secondary-color);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 20px;
    }
    
    .stTextInput input::placeholder {
        color: #a8a8a8;
    }
    
    /* Logout button */
    .logout-button {
        position: fixed;
        top: 20px;
        left: 20px;
        background-color: var(--accent-color);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
            border: none;
            cursor: pointer;
        text-decoration: none;
    }
    
    .logout-button:hover {
        opacity: 0.9;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for chat history if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display header
st.markdown('<h1 class="main-header">✨ Vibe Check Bot</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">let\'s chat about whatever\'s on your mind! 🌿</p>', unsafe_allow_html=True)

# Logout button
st.markdown(
    '<a href="#" class="logout-button">Logout</a>',
    unsafe_allow_html=True
)

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
        st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
user_input = st.text_input("", placeholder="what's on your mind?", key="user_input", label_visibility="collapsed")

if user_input:
            # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get bot response
    response = get_trained_response(user_input)
    
    # Add bot response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            
    # Rerun to update the chat display
    st.experimental_rerun()