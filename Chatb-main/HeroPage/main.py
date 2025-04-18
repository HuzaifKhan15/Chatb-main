import streamlit as st

# Set page config (must be the first Streamlit command)
st.set_page_config(
    page_title="✨ Vibe Check Bot",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

import yaml
import os
import sys
import streamlit_authenticator as stauth
from PIL import Image
import subprocess
import bcrypt
from yaml.loader import SafeLoader
import random
import importlib.util

# Modern Gen Z UI Styling
st.markdown("""
<style>
    /* Modern Gen Z styling with fun colors and vibes */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #FF6B6B;
        --secondary: #4ECDC4;
        --accent: #FFE66D;
        --bg: #1A1A1A;
        --text: #FFFFFF;
        --text-secondary: #B5B5B5;
    }
    
    body {
        font-family: 'Outfit', sans-serif;
        background-color: var(--bg);
        color: var(--text);
        line-height: 1.6;
    }
    
    /* Fun container styling */
    .stApp {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    }
    
    /* Message container */
    .chat-message {
        padding: 1rem;
        border-radius: 20px;
        margin-bottom: 1rem;
        max-width: 80%;
        animation: pop-in 0.3s ease-out;
    }
    
    /* User message */
    .user-message {
        background: var(--primary);
        margin-left: auto;
        border-radius: 20px 20px 5px 20px;
    }
    
    /* Bot message */
    .bot-message {
        background: #2C2C2C;
        margin-right: auto;
        border-radius: 20px 20px 20px 5px;
    }
    
    /* Input box styling */
    .stTextInput input {
        border-radius: 25px !important;
        border: 2px solid var(--primary) !important;
        padding: 1rem !important;
        background: #2C2C2C !important;
        color: white !important;
        font-size: 1rem !important;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 25px !important;
        background: var(--primary) !important;
        color: white !important;
        padding: 0.5rem 2rem !important;
        font-size: 1rem !important;
        border: none !important;
        transition: transform 0.2s !important;
    }
    
    .stButton button:hover {
        transform: scale(1.05) !important;
    }
    
    /* Emoji reactions */
    .emoji-reaction {
        font-size: 1.5rem;
        margin: 0.5rem;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .emoji-reaction:hover {
        transform: scale(1.2);
    }
    
    /* Fun animations */
    @keyframes pop-in {
        0% { transform: scale(0.8); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(45deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1A1A1A;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary);
    }
</style>
""", unsafe_allow_html=True)

import yaml
import os
import sys
import streamlit_authenticator as stauth
from PIL import Image
import subprocess
import bcrypt
from yaml.loader import SafeLoader
import random
import importlib.util
import datetime

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Make sure the config directory exists
os.makedirs(os.path.join(BASE_DIR, "HeroPage", "config"), exist_ok=True)
CONFIG_PATH = os.path.join(BASE_DIR, "HeroPage", "config", "config.yaml")

# Create config file if it doesn't exist
if not os.path.exists(CONFIG_PATH):
    default_config = {
        'credentials': {
            'usernames': {
                'admin': {
                    'email': 'admin@example.com',
                    'name': 'Admin User',
                    'password': bcrypt.hashpw('admin123'.encode(), bcrypt.gensalt()).decode()
                }
            }
        },
        'cookie': {
            'expiry_days': 30,
            'key': 'sunshine_auth',
            'name': 'sunshine_auth_cookie'
        }
    }
    
    with open(CONFIG_PATH, 'w') as file:
        yaml.dump(default_config, file)

# Load configuration
with open(CONFIG_PATH, 'r') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Create the authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

def create_account():
    with st.form("signup_form", clear_on_submit=True):
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h3 style="font-size: 2rem; margin-bottom: 0.8rem; background: linear-gradient(90deg, var(--secondary-light), var(--primary-light)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Create Account ✌️</h3>
            <p style="color: var(--text-secondary); font-size: 1.05rem;">Join our community today</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            new_username = st.text_input("Username", key="new_username", placeholder="Choose a username")
            new_email = st.text_input("Email", key="new_email", placeholder="Your email address")
            new_password = st.text_input("Password", type="password", key="new_password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password", placeholder="Verify your password")
        with col2:
            new_name = st.text_input("Full Name", key="new_name", placeholder="Your full name")
        
        st.markdown("""
        <div style="margin: 1rem 0 1.5rem; background: rgba(255, 255, 255, 0.03); padding: 1rem; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.05);">
            <p style="color: var(--text-secondary); font-size: 0.95rem; display: flex; align-items: center; gap: 10px; margin: 0;">
                <div style="width: 20px; height: 20px; border: 2px solid var(--primary-light); border-radius: 4px; position: relative;">
                    <div style="position: absolute; top: 2px; left: 2px; right: 2px; bottom: 2px; background: var(--primary-light); border-radius: 2px; opacity: 0.5;"></div>
                </div>
                I agree to the <a href="#" style="color: var(--primary-light); text-decoration: none; margin: 0 2px; font-weight: 500;">Terms of Service</a> and <a href="#" style="color: var(--primary-light); text-decoration: none; margin-left: 2px; font-weight: 500;">Privacy Policy</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        signup_button = st.form_submit_button("Create Account")
        
        if signup_button:
            error_occurred = False
            if new_password != confirm_password:
                st.error("Passwords do not match")
                error_occurred = True
            
            if not new_username or not new_name or not new_email or not new_password:
                st.error("All fields required")
                error_occurred = True
                
            # Check if username already exists
            if new_username in config['credentials']['usernames']:
                st.error("Username already exists")
                error_occurred = True
            
            # Only proceed if no errors
            if not error_occurred:
                # Add new user
                config['credentials']['usernames'][new_username] = {
                    'email': new_email,
                    'name': new_name,
                    'password': bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                }
                
                # Save updated config
                with open(CONFIG_PATH, 'w') as file:
                    yaml.dump(config, file)
                    
                st.success("Account created successfully! ✅")
                st.session_state.page = "login"
                st.rerun()

def home_page():
    # Apply custom CSS for Gen Z styling to the entire app
    st.markdown("""
    <style>
        /* Modern Font */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        /* Container styling */
        .home-container {
            background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.18);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
            transition: all 0.3s ease;
        }
        
        .home-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 36px 0 rgba(31, 38, 135, 0.25);
        }
        
        /* Headings */
        .home-title {
            font-weight: 700;
            background: linear-gradient(90deg, #FF9A8B 0%, #FF6A88 55%, #FF99AC 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 15px;
            font-size: 1.8rem;
            letter-spacing: 0.5px;
        }
        
        /* Content styling */
        .home-content {
            font-size: 1rem;
            line-height: 1.6;
            color: #f9f9f9;
        }
        
        /* Button styling */
        .home-button {
            display: inline-block;
            padding: 10px 20px;
            background: linear-gradient(90deg, #FF9A8B 0%, #FF6A88 55%, #FF99AC 100%);
            color: white;
            border: none;
            border-radius: 30px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            margin-top: 15px;
            transition: all 0.3s ease;
            text-decoration: none;
        }
        
        .home-button:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 20px rgba(255, 106, 136, 0.3);
        }
        
        /* Emoji style */
        .emoji {
            font-size: 1.5rem;
            margin-right: 10px;
            vertical-align: middle;
        }
        
        /* Custom bullet points */
        .custom-bullet {
            list-style-type: none;
            padding-left: 0;
        }
        
        .custom-bullet li {
            position: relative;
            padding-left: 25px;
            margin-bottom: 10px;
        }
        
        .custom-bullet li:before {
            content: "✨";
            position: absolute;
            left: 0;
            color: #FF6A88;
        }
        
        /* Animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animated {
            animation: fadeIn 0.8s ease forwards;
        }
        
        .delay-1 {
            animation-delay: 0.2s;
        }
        
        .delay-2 {
            animation-delay: 0.4s;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Home page content
    st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>Welcome to Sunshine Mental Wellness</h1>", unsafe_allow_html=True)
    
    # Two columns for the home page containers
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="home-container animated delay-1">
            <h2 class="home-title">Talk to our Mental Health Assistant 💬</h2>
            <p class="home-content">
                Feeling stressed, anxious, or just need someone to talk to? Our AI mental health assistant is here to listen and provide support.
            </p>
            <ul class="custom-bullet home-content">
                <li>24/7 confidential conversations</li>
                <li>Evidence-based coping strategies</li>
                <li>No judgment, just support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Chat Now", key="chat_btn", use_container_width=True):
            st.session_state.page = "chatbot"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="home-container animated delay-2">
            <h2 class="home-title">Meet Our Mental Health Professionals 🧠</h2>
            <p class="home-content">
                Connect with licensed professionals who can provide personalized care and guidance for your mental health journey.
            </p>
            <ul class="custom-bullet home-content">
                <li>Expert therapists and counselors</li>
                <li>Specialized in various mental health areas</li>
                <li>Personalized treatment plans</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("View Doctors", key="doctor_btn", use_container_width=True):
            st.session_state.page = "doctor"
            st.rerun()

# Function to find the doctor image in multiple locations
def find_doctor_image():
    # This function is now disabled as we're not showing images
    return None

def doctor_page():
    # Simplified doctor page with just a back button
    st.markdown("""
    <div class="header" style="max-width: 800px; margin: 0 auto;">
        <h1>Our Mental Health Professionals</h1>
        <p>Connect with licensed therapists specializing in various mental health areas</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add a back button at the top
    col_back, col_spacer = st.columns([1, 3])
    with col_back:
        if st.button("← Back to Home", key="back_from_doctor", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    
    # Display a message that this feature is coming soon
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; background: rgba(255,255,255,0.05); border-radius: 16px; border: 1px solid rgba(255,255,255,0.1);">
        <h2 style="margin-bottom: 1rem;">Coming Soon!</h2>
        <p style="font-size: 1.2rem; margin-bottom: 1.5rem;">Our doctor directory is currently under development.</p>
        <p>We're working hard to bring you access to qualified mental health professionals.</p>
    </div>
    """, unsafe_allow_html=True)

def get_response(user_input):
    # Convert input to lowercase for easier matching
    input_lower = user_input.lower()
    
    # Mental health focused responses with positive reinforcement
    responses = {
        # Job stress and loss
        "stressed about job": "I hear how overwhelming work stress can be. Remember, your well-being comes first. Here are some ways to cope: 🌟\n1. Take regular breaks\n2. Practice deep breathing\n3. Set clear boundaries\n4. Talk to someone you trust\n5. Focus on what you can control\nWould you like to talk more about what's stressing you? 💛",
        "job stress": "Work stress can feel overwhelming, but remember - you've handled challenges before. Here's what might help: 🌟\n1. Break tasks into smaller steps\n2. Practice self-care\n3. Set realistic goals\n4. Take time to recharge\n5. Remember your worth isn't defined by work\nLet's talk about what's going on. 💫",
        "fired from job": "I'm sorry to hear about your job loss. This can be really tough, but remember - this is just one chapter in your story. Here are some steps forward: 🌟\n1. Allow yourself to feel your emotions\n2. Update your resume\n3. Reach out to your network\n4. Take time to reflect\n5. Remember your skills and strengths\nWould you like to talk about your next steps? 💪",
        "lost my job": "I hear how difficult this time is for you. Remember, your worth isn't defined by your job. Here's how to move forward: 🌟\n1. Process your feelings\n2. Update your skills\n3. Network with others\n4. Take care of yourself\n5. Stay positive and persistent\nYou've got this! 💛",
        
        # Loss of loved ones
        "death of loved one": "I'm so sorry for your loss. Grieving is a personal journey, and it's okay to feel however you feel. Here are some ways to cope: 🌟\n1. Allow yourself to grieve\n2. Talk about your loved one\n3. Take care of yourself\n4. Seek support from others\n5. Remember the good times\nWould you like to share memories of your loved one? 💛",
        "lost someone": "I hear how painful this loss is for you. Grief takes time, and it's okay to feel whatever you're feeling. Here's what might help: 🌟\n1. Express your feelings\n2. Create a memory book\n3. Talk to supportive people\n4. Take things one day at a time\n5. Be gentle with yourself\nWould you like to talk about your loved one? 💫",
        "someone died": "I'm deeply sorry for your loss. Grieving is a natural process, and there's no right way to do it. Here are some ways to cope: 🌟\n1. Share your feelings\n2. Create rituals to remember\n3. Seek support from others\n4. Take care of your health\n5. Be patient with yourself\nWould you like to talk about how you're feeling? 💛",
        
        # School bullying
        "school bully": "I'm so sorry you're experiencing bullying at school. Remember, you don't deserve this treatment. Here are some steps you can take: 🌟\n1. Talk to a trusted teacher or counselor\n2. Document the incidents\n3. Stay close to supportive friends\n4. Practice self-care\n5. Remember your worth isn't defined by their actions\nWould you like to talk more about what's happening? 💛",
        "being bullied at school": "I hear how difficult this is for you. School should be a safe place. Here's what you can do: 🌟\n1. Tell a trusted adult about what's happening\n2. Keep a record of the incidents\n3. Stay with supportive friends\n4. Practice self-care activities\n5. Remember you're not alone in this\nWould you like to discuss how we can handle this situation? 💫",
        "classmates bullying me": "I'm here to support you through this. Remember, their actions say more about them than about you. Here are some ways to cope: 🌟\n1. Build a support network\n2. Focus on your strengths\n3. Practice self-compassion\n4. Document the incidents\n5. Talk to school authorities\nYou're stronger than their words! 💪",
        
        # Workplace bullying
        "office bully": "I'm sorry you're experiencing bullying at work. This is unacceptable. Here are some steps you can take: 🌟\n1. Document all incidents\n2. Report to HR or management\n3. Stay professional\n4. Build a support network\n5. Know your rights\nWould you like to talk more about the situation? 💛",
        "workplace bullying": "I hear how challenging this is. Your workplace should be professional and respectful. Here's what you can do: 🌟\n1. Keep detailed records\n2. Report to appropriate channels\n3. Stay focused on your work\n4. Seek support from colleagues\n5. Know your company's policies\nRemember, you deserve respect! 💫",
        "boss bullying me": "I'm sorry you're experiencing this from someone in authority. This is not okay. Here are some steps: 🌟\n1. Document all interactions\n2. Report to HR or higher management\n3. Stay professional\n4. Know your rights\n5. Consider seeking legal advice\nWould you like to discuss your options? 💪",
        
        # Online bullying
        "cyberbully": "I'm sorry you're experiencing online bullying. This can be especially hurtful. Here's what you can do: 🌟\n1. Don't respond to the bully\n2. Save evidence (screenshots)\n3. Block and report the person\n4. Talk to someone you trust\n5. Take breaks from social media\nRemember, you're not alone in this! 💛",
        "online bullying": "I hear how difficult this is. The online world should be safe for everyone. Here are some steps: 🌟\n1. Document all messages\n2. Report to platform moderators\n3. Block the person\n4. Take care of your mental health\n5. Talk to someone you trust\nWould you like to discuss how you're feeling? 💫",
        
        # General bullying support
        "i'm being bullied": "I'm so sorry you're going through this. Remember, their words don't define your worth. You are unique, valuable, and deserving of respect. Would you like to talk about what's happening? 💛",
        "i'm getting bullied": "That's really tough, but remember - you are not alone in this. Your strength is greater than their words. Would you like to discuss how we can handle this situation? 🌟",
        "people are bullying me": "I'm here to support you. Remember, you are worthy of love and respect. Let's talk about how you're feeling and what we can do. You're stronger than you think! 💪",
        
        # Peace and mental health tips
        "tips for peace": "Here are some ways to find peace: 🌟\n1. Practice deep breathing exercises\n2. Try meditation for 5-10 minutes daily\n3. Spend time in nature\n4. Keep a gratitude journal\n5. Listen to calming music\n6. Practice mindfulness in daily activities\n7. Connect with loved ones\n8. Take regular breaks from screens\n9. Exercise regularly\n10. Get enough sleep\nRemember, peace is a journey, not a destination. Start with small steps! 💫",
        "how to find peace": "Finding peace starts with small steps: 🌟\n1. Accept your feelings without judgment\n2. Create a peaceful space at home\n3. Practice self-compassion\n4. Set healthy boundaries\n5. Focus on the present moment\n6. Let go of things you can't control\n7. Find activities that bring you joy\n8. Practice forgiveness\n9. Connect with nature\n10. Be kind to yourself\nPeace comes from within - you've got this! 💛",
        
        # Crisis situations
        "i want to die": "I'm really concerned about what you're going through. Your life is valuable and important. Please, let's talk about this. You're not alone, and there are people who care about you deeply. Would you like to talk about what's making you feel this way? 💛",
        "i wanna die": "I hear how much pain you're in right now. Please know that your life matters, and there are people who want to help you through this. Let's talk about what's going on. You don't have to face this alone. 💛",
        "i want to kill myself": "I'm very concerned about you. Your life is precious, and there are people who care about you. Please, let's talk about this. You don't have to go through this alone. Would you like to share what's making you feel this way? 💛",
        "i'm suicidal": "I'm really worried about you. Your life is valuable, and there are people who want to help you through this difficult time. Let's talk about what's going on. You're not alone in this. 💛",
        
        # Hopelessness and despair
        "i don't know what to do": "I hear how lost you're feeling right now. It's okay to feel this way, but remember - you don't have to figure everything out alone. Let's talk through this together. What's been going on? 💛",
        "i feel hopeless": "I understand you're feeling hopeless right now. Remember, feelings are temporary, even when they feel overwhelming. Let's talk about what's making you feel this way. You're stronger than you think. 🌟",
        "i can't go on": "I hear how difficult things are for you right now. Please know that you don't have to face this alone. Let's talk about what's going on. There are people who care about you and want to help. 💛",
        "i give up": "I understand you're feeling overwhelmed right now. It's okay to feel this way, but remember - you don't have to give up. Let's talk about what's making you feel this way. You're stronger than you think. 🌟",
        
        # Depression related
        "i'm depressed": "I hear you, and I want you to know that your feelings are valid. But remember, even in the darkest moments, there's always a way forward. You're stronger than you think! 💪 Would you like to talk about what's been going on? 💛",
        "i feel depressed": "I'm here for you. Remember, every storm eventually passes, and you have the strength to weather this one. Let's take it one step at a time. What's been on your mind lately? 🌟",
        "i'm feeling down": "It's okay to feel down sometimes. Just remember, you've overcome challenges before, and you can do it again. Would you like to share what's been bothering you? I'm here to listen. 💫",
        
        # Sadness related
        "i'm sad": "I'm here for you. Remember, it's okay to feel sad, but don't forget that brighter days are ahead. Would you like to talk about what's making you feel this way? 💛",
        "i feel sad": "Your feelings are valid, and it's okay to feel this way. Just remember, every emotion is temporary, and you have the strength to get through this. Let's talk about what's on your mind. 🌟",
        "i'm feeling sad": "It's okay to feel this way. Remember, you've overcome sadness before, and you can do it again. Would you like to share what's been bothering you? 💫",
        
        # General emotional support
        "i need help": "I'm here to help you. Remember, asking for help is a sign of strength, not weakness. What's going on? You're not alone in this. 💛",
        "i feel lost": "I'm here to help you find your way. Remember, even when you feel lost, you're still moving forward. Would you like to talk about what's making you feel this way? 💫",
        
        # Greetings and basic responses
        "hi": "Hey there! 👋 How are you feeling today? Remember, every day is a new opportunity for growth!",
        "hello": "Hi! I'm here to listen and support you. How can I help you today? 💛",
        "help": "I'm here to chat about anything that's on your mind - your feelings, struggles, or just to listen. Remember, you're stronger than you think! 💫",
        "bye": "Take care! Remember, you're capable of amazing things! Stay strong and keep shining! ✌️",
        "thanks": "You're welcome! Remember, I'm always here to support you. Keep believing in yourself! 💛"
    }
    
    # Check for exact matches first
    if input_lower in responses:
        return responses[input_lower]
    
    # Check for partial matches with more context
    for key in responses:
        if key in input_lower:
            return responses[key]
    
    # Check for emotional keywords with positive reinforcement
    emotional_keywords = {
        "job": "I hear you're going through a tough time at work. Remember, your worth isn't defined by your job. Would you like to talk about what's happening? 💛",
        "work": "Work can be challenging, but remember - you've overcome challenges before. Let's talk about what's going on. 💫",
        "fired": "I'm sorry to hear about your job loss. This is a difficult time, but remember - this is just one chapter in your story. Would you like to talk about your next steps? 💪",
        "death": "I'm so sorry for your loss. Grieving is a personal journey, and it's okay to feel however you feel. Would you like to talk about it? 💛",
        "died": "I hear how painful this loss is for you. Would you like to share memories of your loved one? 💫",
        "loss": "I'm here to support you through this difficult time. Would you like to talk about how you're feeling? 💛",
        "bully": "I'm sorry you're experiencing this. Remember, you are worthy of love and respect. Let's talk about what's happening and how we can handle it. 🌟",
        "bullied": "I hear you're going through a tough time. Remember, you don't deserve this treatment. Would you like to talk about what's happening? 💛",
        "harassment": "I'm sorry you're experiencing this. This is not okay. Let's talk about what's happening and how we can address it. 💪",
        "teasing": "I understand how hurtful this can be. Remember, their words don't define your worth. Would you like to talk about it? 💫",
        "die": "I'm really concerned about what you're going through. Your life is valuable and important. Please, let's talk about this. You're not alone, and there are people who care about you deeply. 💛",
        "suicide": "I'm very worried about you. Your life matters, and there are people who want to help you through this difficult time. Let's talk about what's going on. You don't have to face this alone. 💛",
        "kill myself": "I'm deeply concerned about you. Please know that your life is precious, and there are people who care about you. Let's talk about what's making you feel this way. 💛",
        "end it all": "I hear how much pain you're in right now. Please know that your life matters, and there are people who want to help you through this. Let's talk about what's going on. 💛",
        "depress": "I hear you're feeling down. Remember, even in the darkest moments, there's always hope. Would you like to talk about what's been going on? 💛",
        "sad": "It's okay to feel sad. Remember, brighter days are ahead. Would you like to share what's on your mind? 💫",
        "hopeless": "I understand you're feeling hopeless right now. Remember, feelings are temporary, even when they feel overwhelming. Let's talk about what's making you feel this way. 💛",
        "worthless": "You are not worthless. You are valuable and important. Let's talk about what's making you feel this way. 💛",
        "alone": "You are not alone in this. I'm here to listen and support you. Let's talk about what's going on. 💫"
    }
    
    for keyword in emotional_keywords:
        if keyword in input_lower:
            return emotional_keywords[keyword]
    
    # Default supportive and motivational responses
    default_responses = [
        "I'm here to listen. Remember, you're stronger than you think! How are you feeling about this? 💛",
        "That sounds tough, but I believe in your ability to handle this. Would you like to talk more about it? 🌟",
        "I hear you. Remember, every challenge is an opportunity for growth. Let's work through this together. 💪",
        "Your feelings are valid, and you're doing great by reaching out. What's been on your mind? 💫",
        "I'm here to support you. Remember, you're capable of amazing things! How can I help? 💛",
        "Let's talk about how you're feeling. Remember, you're not alone in this journey. 🌟",
        "I'm listening. Remember, every step forward, no matter how small, is progress. What's been going on? 💫",
        "You're not alone in this. Remember, you have the strength to overcome challenges. Let's talk about it. 💛",
        "I'm here for you. Remember, you're doing better than you think. What's been bothering you? 🌟",
        "Let's work through this together. Remember, you're stronger than any challenge you face. 💪"
    ]
    
    return random.choice(default_responses)

def launch_chatbot():
    st.title("✨ Vibe Check Bot")
    st.markdown("### let's chat about whatever's on your mind! 🌈")
    
    # Initialize chat history in session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(f"""
                <div class="chat-message {'user-message' if message['role'] == 'user' else 'bot-message'}">
                    {message["content"]}
                </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("💭 what's on your mind?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(f"""
                <div class="chat-message user-message">
                    {prompt}
                </div>
            """, unsafe_allow_html=True)
        
        # Get bot response
        response = get_response(prompt)
        
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display bot response
        with st.chat_message("assistant"):
            st.markdown(f"""
                <div class="chat-message bot-message">
                    {response}
                </div>
            """, unsafe_allow_html=True)
        
        # Rerun to update the display
        st.rerun()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "login"

# Main app logic
if st.session_state.page == "login":
    st.markdown("""
    <div class="auth-container" style="max-width: 800px; margin: 0 auto; padding: 0; text-align: center;">
        <div class="logo" style="margin-top: 2px; padding-top: 0;">
            <span class="logo-icon" style="font-size: 3.5rem;">☀️</span>
            <span class="logo-text" style="font-size: 3.5rem;">Sunshine</span>
        </div>
        <p style="text-align: center; color: var(--text-light); margin-top: 0; margin-bottom: 1rem; font-size: 1.5rem; max-width: 600px; margin-left: auto; margin-right: auto;">Mental wellness companion for a brighter tomorrow ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                st.markdown("""
                <div style="text-align: center; margin-bottom: 2.5rem;">
                    <h3 style="font-size: 2.2rem; margin-bottom: 0.8rem; background: linear-gradient(90deg, var(--accent), var(--primary-light)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Welcome Back! 👋</h3>
                    <p style="color: var(--text-secondary); font-size: 1.05rem;">Good to see you again</p>
                </div>
                """, unsafe_allow_html=True)
                
                username = st.text_input("Username", placeholder="Your username")
                password = st.text_input("Password", type="password", placeholder="Your password")
                
                st.markdown("""
                <div style="display: flex; justify-content: space-between; align-items: center; margin: 1.2rem 0 1.5rem; background: rgba(255, 255, 255, 0.03); padding: 0.8rem 1rem; border-radius: 12px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div class="custom-checkbox">
                            <div class="custom-checkbox-inner"></div>
                        </div>
                        <span style="color: var(--text-secondary); font-size: 0.95rem; font-weight: 500;">Remember me</span>
                    </div>
                    <div>
                        <a href="#" style="color: var(--primary-light); font-size: 0.95rem; text-decoration: none; font-weight: 600; transition: all 0.2s ease; position: relative; padding-bottom: 2px;">
                            Forgot password?
                            <span style="position: absolute; bottom: 0; left: 0; width: 100%; height: 1px; background: linear-gradient(90deg, transparent, var(--primary-light), transparent); transition: all 0.3s ease;"></span>
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                login_button = st.form_submit_button("Sign In")
                
                if login_button:
                    try:
                        # We'll handle authentication manually since we're using a custom form
                        if username in config['credentials']['usernames']:
                            user_hash = config['credentials']['usernames'][username]['password']
                            if bcrypt.checkpw(password.encode(), user_hash.encode()):
                                # Set session state
                                st.session_state.username = username
                                st.session_state.name = config['credentials']['usernames'][username]['name']
                                st.session_state.authentication_status = True
                                st.session_state.page = "home"
                                st.rerun()
                            else:
                                st.error("Incorrect password")
                        else:
                            st.error("Username not found")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        st.info("Try using username: admin, password: admin123")
                
                st.markdown("""
                <div style="text-align: center; margin-top: 2.5rem; font-size: 0.95rem; color: var(--text-secondary);">
                    New here? <span style="font-weight: 600; color: var(--primary-light); background: linear-gradient(90deg, var(--primary-light), var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Switch to Sign Up</span>
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            with st.form("signup_form", clear_on_submit=True):
                st.markdown("""
                <div style="text-align: center; margin-bottom: 2.5rem;">
                    <h3 style="font-size: 2.2rem; margin-bottom: 0.8rem; background: linear-gradient(90deg, var(--secondary-light), var(--primary-light)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Join Us Today ✌️</h3>
                    <p style="color: var(--text-secondary); font-size: 1.05rem;">Create your account in seconds</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    new_username = st.text_input("Username", key="new_username", placeholder="Pick a cool username")
                    new_email = st.text_input("Email", key="new_email", placeholder="Your email")
                    new_password = st.text_input("Password", type="password", key="new_password", placeholder="Super secret password")
                    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password", placeholder="Confirm your password")
                with col2:
                    new_name = st.text_input("Full Name", key="new_name", placeholder="Your name")
                
                st.markdown("""
                <div style="margin: 1.2rem 0 1.8rem; background: rgba(255, 255, 255, 0.03); padding: 1.2rem; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.05);">
                    <p style="color: var(--text-secondary); font-size: 0.95rem; display: flex; align-items: center; gap: 10px; margin: 0;">
                        <div class="custom-checkbox">
                            <div class="custom-checkbox-inner"></div>
                        </div>
                        I agree to the <a href="#" style="color: var(--primary-light); text-decoration: none; margin: 0 2px; font-weight: 600; position: relative; padding-bottom: 2px;">
                            Terms 
                            <span style="position: absolute; bottom: 0; left: 0; width: 100%; height: 1px; background: linear-gradient(90deg, transparent, var(--primary-light), transparent);"></span>
                        </a> 
                        and 
                        <a href="#" style="color: var(--primary-light); text-decoration: none; margin-left: 2px; font-weight: 600; position: relative; padding-bottom: 2px;">
                            Privacy Policy
                            <span style="position: absolute; bottom: 0; left: 0; width: 100%; height: 1px; background: linear-gradient(90deg, transparent, var(--primary-light), transparent);"></span>
                        </a>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                signup_button = st.form_submit_button("Create Account")
                
                if signup_button:
                    error_occurred = False
                    if new_password != confirm_password:
                        st.error("Passwords do not match")
                        error_occurred = True
                    
                    if not new_username or not new_name or not new_email or not new_password:
                        st.error("All fields required")
                        error_occurred = True
                        
                    # Check if username already exists
                    if new_username in config['credentials']['usernames']:
                        st.error("Username already exists")
                        error_occurred = True
                    
                    # Only proceed if no errors
                    if not error_occurred:
                        # Add new user
                        config['credentials']['usernames'][new_username] = {
                            'email': new_email,
                            'name': new_name,
                            'password': bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                        }
                        
                        # Save updated config
                        with open(CONFIG_PATH, 'w') as file:
                            yaml.dump(config, file)
                            
                        st.success("Account created successfully! ✅")
                        st.session_state.page = "login"
                        st.rerun()
                
                st.markdown("""
                <div style="text-align: center; margin-top: 2.5rem; font-size: 0.95rem; color: var(--text-secondary);">
                    Already have an account? <span style="font-weight: 600; color: var(--primary-light); background: linear-gradient(90deg, var(--primary-light), var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Switch to Login</span>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer">
        <p>© 2023 Sunshine Mental Wellness. All rights reserved.</p>
        <div style="display: flex; justify-content: center; gap: 1.5rem; margin-top: 0.8rem;">
            <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s ease;">About</a>
            <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s ease;">Privacy</a>
            <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s ease;">Terms</a>
            <a href="#" style="color: var(--text-secondary); text-decoration: none; font-size: 0.95rem; transition: color 0.2s ease;">Contact</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "home":
    # Display logout in sidebar
    with st.sidebar:
        if st.button("Logout"):
            st.session_state.page = "login"
            st.session_state.authentication_status = False
            st.rerun()
    
    home_page()
    
elif st.session_state.page == "doctor":
    with st.sidebar:
        if st.button("Logout"):
            st.session_state.page = "login"
            st.session_state.authentication_status = False
            st.rerun()
    
    doctor_page()
    
elif st.session_state.page == "chatbot":
    with st.sidebar:
        if st.button("Logout"):
            st.session_state.page = "login"
            st.session_state.authentication_status = False
            st.rerun()
    
    launch_chatbot() 