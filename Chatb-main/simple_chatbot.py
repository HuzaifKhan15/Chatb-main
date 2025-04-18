import streamlit as st
import json
import random
from datetime import datetime

# Enhanced AI-like response patterns
RESPONSES = {
    "greeting": [
        "Hello! I'm here to help you with anything you'd like to discuss. How can I assist you today?",
        "Hi there! I'm ready to engage in a meaningful conversation. What would you like to talk about?",
        "Greetings! I'm here to provide thoughtful responses and support. What's on your mind?"
    ],
    "feeling_sad": [
        "I understand you're feeling down. It's completely normal to experience these emotions. Would you like to explore what might be contributing to these feelings? I'm here to listen and help you process them.",
        "I hear your sadness, and I want you to know that your feelings are valid. Sometimes, talking about what's bothering us can help us understand and process our emotions better. Would you like to share more about what's on your mind?",
        "I'm sorry to hear you're feeling this way. Emotional pain can be challenging to navigate. Let's work together to understand what might be causing these feelings and explore ways to help you feel better."
    ],
    "feeling_happy": [
        "That's wonderful to hear! Positive emotions are important for our well-being. Would you like to explore what's contributing to your happiness? Sometimes understanding what brings us joy can help us cultivate more of these moments.",
        "I'm glad you're experiencing positive emotions! It's great that you're feeling good. Would you like to discuss what's bringing you this happiness? Understanding our sources of joy can help us maintain and create more positive experiences.",
        "It's fantastic that you're feeling happy! Positive emotions are essential for our mental health. Let's explore what's contributing to your happiness and how we might be able to maintain or enhance these feelings."
    ],
    "feeling_anxious": [
        "I understand you're feeling anxious. Anxiety can be overwhelming, but it's important to remember that these feelings are temporary. Would you like to explore some coping strategies or discuss what might be triggering your anxiety?",
        "Anxiety can be challenging to manage, but you're not alone. Let's work together to understand what might be causing these feelings and explore some techniques that could help you feel more grounded and in control.",
        "I hear your anxiety, and I want you to know that it's okay to feel this way. Sometimes, breaking down what's causing our anxiety can help us manage it better. Would you like to explore this together?"
    ],
    "relationships": [
        "Relationships can be complex and sometimes challenging to navigate. Would you like to explore the dynamics of your relationship and discuss ways to improve communication or address any concerns?",
        "I understand that relationships can bring both joy and challenges. Let's examine the situation together and explore ways to strengthen your connection or address any issues you're facing.",
        "Relationships are an important part of our lives, and it's normal to have questions or concerns about them. Would you like to discuss what's on your mind and explore ways to enhance your relationship?"
    ],
    "school_work": [
        "Academic and work-related stress can be significant. Let's explore what's causing your stress and discuss some strategies to manage your workload more effectively while maintaining your well-being.",
        "I understand that school/work can be demanding. Would you like to discuss specific challenges you're facing and explore some techniques to help you manage your responsibilities while taking care of yourself?",
        "Balancing academic or work responsibilities with self-care can be challenging. Let's work together to identify what's causing your stress and develop a plan to help you manage it more effectively."
    ],
    "self_care": [
        "Self-care is essential for maintaining our mental and physical well-being. Would you like to explore different self-care practices and discuss how to incorporate them into your daily routine?",
        "Taking care of yourself is crucial for your overall health. Let's discuss what self-care means to you and explore ways to make it a regular part of your life. What practices have you found helpful in the past?",
        "Self-care is an important aspect of maintaining balance in our lives. Would you like to explore different self-care strategies and discuss how to make them work for your specific needs and lifestyle?"
    ],
    "motivation": [
        "Motivation can fluctuate, and that's completely normal. Let's explore what drives you and discuss strategies to help you maintain or regain your motivation. What goals are you working towards?",
        "I understand that staying motivated can be challenging at times. Would you like to explore what inspires you and discuss ways to keep that motivation going? Let's break down your goals and create a plan that works for you.",
        "Motivation is often connected to our values and goals. Let's examine what's important to you and discuss ways to maintain your drive. What aspects of your life or work are you most passionate about?"
    ],
    "default": [
        "I'm here to help you explore your thoughts and feelings. Could you tell me more about what's on your mind? The more context you provide, the better I can assist you.",
        "I want to understand your perspective better. Could you elaborate on what you're thinking or feeling? This will help me provide more meaningful support and guidance.",
        "I'm interested in hearing more about your experience. Would you like to share additional details? This will help me provide more relevant and helpful responses."
    ]
}

# Enhanced keyword detection
KEYWORDS = {
    "greeting": ["hi", "hello", "hey", "sup", "yo", "what's up", "greetings", "good morning", "good afternoon", "good evening"],
    "feeling_sad": ["sad", "depressed", "down", "unhappy", "cry", "tears", "hurt", "lonely", "empty", "hopeless", "worthless"],
    "feeling_happy": ["happy", "good", "great", "wonderful", "amazing", "excited", "joy", "thrilled", "delighted", "ecstatic", "content"],
    "feeling_anxious": ["anxious", "worried", "nervous", "stressed", "panic", "overwhelm", "fear", "scared", "tense", "uneasy", "apprehensive"],
    "relationships": ["friend", "partner", "relationship", "breakup", "family", "love", "dating", "marriage", "divorce", "conflict", "communication"],
    "school_work": ["school", "work", "study", "exam", "project", "deadline", "assignment", "career", "job", "college", "university"],
    "self_care": ["self care", "relax", "meditate", "yoga", "sleep", "rest", "chill", "wellness", "health", "exercise", "mindfulness"],
    "motivation": ["motivated", "goal", "dream", "future", "plan", "achieve", "success", "ambition", "purpose", "drive", "inspiration"]
}

def get_response(user_input):
    input_lower = user_input.lower()
    
    # Check for keywords in each category
    for category, keywords in KEYWORDS.items():
        if any(keyword in input_lower for keyword in keywords):
            return random.choice(RESPONSES[category])
    
    return random.choice(RESPONSES["default"])

def main():
    # Set page config with dark theme
    st.set_page_config(
        page_title="Vibe Check - Your Gen Z Chatbot",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for dark theme and complex styling
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            color: #ffffff;
        }
        .stChatMessage {
            border-radius: 20px;
            padding: 15px;
            margin: 10px 0;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .stTextInput>div>div>input {
            border-radius: 20px;
            padding: 12px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #ffffff;
        }
        .css-1d391kg {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .stButton>button {
            border-radius: 20px;
            background: linear-gradient(135deg, #6e45e2 0%, #88d3ce 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #88d3ce 0%, #6e45e2 100%);
        }
        h1 {
            color: #ffffff;
            text-align: center;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .stMarkdown {
            color: #ffffff;
        }
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #6e45e2 0%, #88d3ce 100%);
            border-radius: 10px;
        }
        /* Glowing effect for messages */
        .stChatMessage:hover {
            box-shadow: 0 0 15px rgba(110, 69, 226, 0.3);
            transition: all 0.3s ease;
        }
        /* Custom chat input placeholder */
        .stTextInput>div>div>input::placeholder {
            color: rgba(255, 255, 255, 0.5);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title with gradient text
    st.markdown("""
        <h1 style="
            background: linear-gradient(135deg, #6e45e2 0%, #88d3ce 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
            margin-bottom: 30px;
        ">
            ✨ Vibe Check - Your Gen Z Chatbot ✨
        </h1>
    """, unsafe_allow_html=True)
    
    # Add a decorative line
    st.markdown("""
        <div style="
            height: 2px;
            background: linear-gradient(90deg, transparent, #6e45e2, #88d3ce, transparent);
            margin: 20px 0;
            border-radius: 2px;
        "></div>
    """, unsafe_allow_html=True)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages with modern styling
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input with modern styling
    if prompt := st.chat_input("What's the vibe? Tell me what's up! ✨"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get and display assistant response
        response = get_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

if __name__ == "__main__":
    main() 