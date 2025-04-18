import streamlit as st
import json
import random
from datetime import datetime

# Professional and friendly response templates
RESPONSES = {
    "greeting": [
        "Hello! I'm here to help. How can I assist you today?",
        "Hi there! I'm ready to chat. What's on your mind?",
        "Welcome! I'm here to support you. How can I help?"
    ],
    "general_help": [
        "I'd be happy to help with that. Could you tell me more about what you're looking for?",
        "I understand you need assistance. Let me help you with that.",
        "I'm here to support you. What specific information would you like?"
    ],
    "mental_health": [
        "I'm here to listen and support you. Would you like to share more about how you're feeling?",
        "Your feelings are important. I'm here to help you process them.",
        "It's okay to feel this way. Let's talk about what's on your mind."
    ],
    "professional": [
        "Based on your query, I can provide some professional insights.",
        "From a professional perspective, here's what I can suggest.",
        "Let me offer some professional guidance on this matter."
    ],
    "friendly": [
        "I'm glad you reached out! Let's work through this together.",
        "You're not alone in this. I'm here to help you figure things out.",
        "I appreciate you sharing this with me. Let's find a solution together."
    ],
    "closing": [
        "Is there anything else you'd like to discuss?",
        "I'm here if you need anything else.",
        "Feel free to ask if you have more questions."
    ]
}

def get_response(user_input):
    # Convert input to lowercase for easier matching
    input_lower = user_input.lower()
    
    # Check for specific keywords and respond accordingly
    if any(word in input_lower for word in ["hi", "hello", "hey"]):
        return random.choice(RESPONSES["greeting"])
    elif any(word in input_lower for word in ["help", "assist", "support"]):
        return random.choice(RESPONSES["general_help"])
    elif any(word in input_lower for word in ["feel", "anxious", "stress", "worried"]):
        return random.choice(RESPONSES["mental_health"])
    elif any(word in input_lower for word in ["professional", "expert", "advice"]):
        return random.choice(RESPONSES["professional"])
    else:
        # Default friendly response
        return random.choice(RESPONSES["friendly"])

def main():
    st.set_page_config(
        page_title="Professional Chat Assistant",
        page_icon="💬",
        layout="wide"
    )
    
    st.title("Professional Chat Assistant")
    st.write("I'm here to help you in a professional and friendly manner.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to discuss?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get and display assistant response
        response = get_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

if __name__ == "__main__":
    main() 