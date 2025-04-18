import os
import streamlit as st
import random
import re
import json
from datetime import datetime
from dotenv import load_dotenv
from resources import CRISIS_RESOURCES, COPING_STRATEGIES, SELF_CARE_REMINDERS, WARNING_SIGNS
from earkick_responses import EARKICK_RESPONSES

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

# Custom function to create resource cards
def resource_card(title, content, emoji="💡"):
    st.markdown(f"""
    <div class="resource-card">
        <h3><span class="emoji-heading">{emoji}</span> {title}</h3>
        {content}
    </div>
    """, unsafe_allow_html=True)

# Custom function to display affirmations
def display_affirmation(text):
    st.markdown(f"""
    <div class="affirmation">
        "{text}"
    </div>
    """, unsafe_allow_html=True)

# Function to check for crisis keywords
def check_for_crisis_keywords(text):
    text = text.lower()
    crisis_keywords = [
        # Direct expressions
        "suicide", "kill myself", "end my life", "hurt myself", "harm myself", 
        "don't want to live", "want to die", "better off dead", "no point in living",
        "i don't want to be here anymore", "i wish i could disappear", "i want it all to stop",
        "i don't see the point of life", "tired of existing", "i want to give up",
        
        # Passive or subtle expressions
        "tired of everything", "nothing makes sense anymore", "every day feels the same",
        "going through the motions", "don't feel anything anymore", "i'm a burden",
        "they'd be better off without me", "better without me",
        
        # Detached expressions
        "life feels pointless", "lost all interest", "don't care what happens to me",
        "feel so empty inside", "feel empty",
        
        # Masked by humor
        "waiting for a bus to hit me", "if i don't wake up tomorrow", "what's the point, we all die",
        "dark comedy at this point",
        
        # Existential thoughts
        "what's the purpose of all this", "why am i even alive", "not meant to be here",
        "i was just a mistake", "i don't feel like living"
    ]
    
    # More sensitive detection - check for presence of keywords
    for keyword in crisis_keywords:
        if keyword in text:
            return True, "self_harm"
            
    # Check for violent thoughts
    violent_keywords = [
        # Direct & Explicit
        "want to kill", "kill them", "going to kill", "gonna kill", "end them", "deserve to die",
        "wish i could strangle", "beat them up", "hurt them", "harm them", "destroy them",
        
        # Anger Masked as Metaphor
        "might lose control", "one second away from snapping", "pushing me over the edge",
        "burn everything down", "going to explode", "about to snap",
        
        # Humor as a Shield
        "jail would be worth it", "commit a crime", "catch them outside",
        
        # Passive but Dangerous
        "fantasizing about hurting", "can't stop thinking about revenge", "watch them suffer"
    ]
    
    for keyword in violent_keywords:
        if keyword in text:
            return True, "violent_thoughts"
    
    return False, None

# Function to check for specific issues in the text
def detect_issue(text):
    """Detect the primary issue or topic from the user input"""
    text = text.lower()
    
    # Check for specific mental health issues first
    depression_keywords = ["depress", "sad", "empty", "hopeless", "meaningless", "no purpose", "no point", "pointless", "can't feel", "don't feel anything", "don't care anymore", "tired of living", "don't see a future"]
    anxiety_keywords = ["anxi", "worry", "stress", "panic", "nervous", "overwhelm", "frightened", "scared", "terrified", "fear", "phobia", "can't relax", "always on edge"]
    sleep_keywords = ["insomnia", "can't sleep", "trouble sleeping", "nightmares", "always tired", "exhausted", "fatigue", "sleep"]
    trauma_keywords = ["trauma", "ptsd", "flashback", "abuse", "assault", "attack", "violent", "accident", "death", "loss"]
    relationship_keywords = ["relationship", "partner", "marriage", "spouse", "boyfriend", "girlfriend", "dating", "breakup", "divorce", "family", "parent", "child", "friend", "coworker", "colleague"]
    loneliness_keywords = ["lonely", "alone", "isolated", "no friends", "no one understands", "nobody cares", "no support", "abandoned"]
    
    # Enhanced work-related keywords with specific subcategories
    work_stress_keywords = ["job stress", "workplace stress", "stressed at work", "work pressure", "job pressure", "demanding job", "toxic workplace", "workplace anxiety", "job anxiety", "stressful job", "work stress", "job is stressful", "hate my job", "exhausted from work", "overwhelmed at work", "workplace bullying", "difficult boss", "bad manager", "hostile work", "unrealistic deadlines", "too much work"]
    career_change_keywords = ["change career", "new career", "career change", "switch jobs", "different field", "career shift", "career move", "career transition", "find new job", "quit my job", "leave my job", "resign", "career path", "career direction", "career advice", "hate my career", "wrong profession", "wrong field"]
    work_life_balance_keywords = ["work life balance", "no free time", "always working", "no personal time", "work too much", "workaholic", "no time for myself", "no time for family", "work on weekends", "work after hours", "boundaries with work", "job taking over", "life revolves around work", "work obsessed", "burnout", "burning out", "no separation between work and life"]
    
    self_esteem_keywords = ["hate myself", "ugly", "worthless", "failure", "not good enough", "can't do anything right", "stupid", "loser", "pathetic", "unlovable", "useless", "waste of"]
    
    # Add new categories for personal experiences
    childhood_trauma_keywords = ["childhood", "growing up", "when i was young", "as a child", "my parents", "my father", "my mother", "my family", "raised", "upbringing", "neglect", "abandon", "early years"]
    relationship_loss_keywords = ["broke up", "break up", "left me", "divorce", "separated", "passed away", "died", "lost him", "lost her", "missing", "grief", "ex", "widow", "no longer together", "no longer with me"]
    identity_struggle_keywords = ["who am i", "identity", "purpose", "meaning", "gender", "sexuality", "orientation", "question who", "true self", "authentic self", "real me", "meant to be", "finding myself", "true identity"]
    life_transition_keywords = ["change", "moving", "transition", "new job", "graduate", "graduation", "retire", "retirement", "baby", "parent", "marriage", "divorce", "career change", "big decision", "crossroads", "turning point"]
    
    # Check for deeper personal experience issues first
    if any(keyword in text for keyword in childhood_trauma_keywords) and any(keyword in text for keyword in ["trauma", "abuse", "hurt", "pain", "difficult", "bad", "terrible", "awful"]):
        return "childhood_trauma"
    elif any(keyword in text for keyword in relationship_loss_keywords):
        return "relationship_loss"
    elif any(keyword in text for keyword in identity_struggle_keywords):
        return "identity_struggle"
    elif any(keyword in text for keyword in life_transition_keywords):
        return "life_transition"
    
    # Check work-related issues with more specific categories
    elif any(keyword in text for keyword in work_stress_keywords):
        return "work_stress"
    elif any(keyword in text for keyword in career_change_keywords):
        return "career_change"
    elif any(keyword in text for keyword in work_life_balance_keywords):
        return "work_life_balance"
    # Then check for more general issues
    elif any(keyword in text for keyword in depression_keywords):
        return "depression"
    elif any(keyword in text for keyword in anxiety_keywords):
        return "anxiety"
    elif any(keyword in text for keyword in sleep_keywords):
        return "sleep"
    elif any(keyword in text for keyword in trauma_keywords):
        return "trauma"
    elif any(keyword in text for keyword in relationship_keywords):
        return "relationship"
    elif any(keyword in text for keyword in loneliness_keywords):
        return "loneliness"
    elif any(keyword in text for keyword in self_esteem_keywords):
        return "self_esteem"
    else:
        return "general"

# Function to detect conversation type
def detect_conversation_type(text):
    text = text.lower()
    
    # Greetings
    greetings = ["hello", "hi ", "hi,", "hi!", "hi.", "hey", "good morning", "good afternoon", "good evening", "greetings", "what's up", "howdy", "sup", "yo", "heya", "hiya"]
    
    # First check for "hi" variations with multiple i's (hii, hiii, hiiii, etc.)
    hi_pattern = re.compile(r'^hi+$|^hi+[.!,\s]')
    if hi_pattern.match(text.strip()):
        return "greeting"
    
    # Then check for the other standard greetings
    for phrase in greetings:
        if text.startswith(phrase):
            return "greeting"
    
    # How are you questions
    how_are_you = ["how are you", "how are you doing", "how's it going", "how have you been", "how's your day", "how are things", "what's new", "how's everything", "how's life", "what's good", "how u doin", "how r u", "wyd", "whats up", "vibes check"]
    
    # How the bot feels questions
    feeling_questions = ["how do you feel", "are you feeling", "are you ok", "are you okay", "are you good", "are you well", "are you happy", "are you sad", "u good", "you alright", "you okay"]
    
    # Gratitude expressions
    gratitude = ["thank", "thanks", "appreciate", "grateful", "helpful", "you're great", "you're amazing", "ur awesome", "tysm", "thx", "ty", "ily"]
    
    # Questions about the bot
    about_bot = ["who are you", "what are you", "are you a", "are you human", "are you real", "are you a bot", "are you ai", "what kind of", "tell me about yourself", "about yourself", "r u a bot", "r u real", "what r u"]
    
    # Help requests - expanded with casual and Gen Z variations
    help_requests = [
        "help me", "i need help", "can you help", "help with", "assist me", "need advice", "give me advice", 
        "what should i do", "what can i do", "need some help", "i'm stuck", "stuck", "assist", "guidance", 
        "a little assistance", "lend me a hand", "walk me through", "back me up", "i have no idea", 
        "sos", "save me", "brain not braining", "help??", "i messed up", "yooo i need", "lifeline", 
        "help me out", "need guidance", "need a miracle", "pls help", "plz help", "halp", "hlp"
    ]
    
    # Problem statements
    problem_statements = ["i have a problem", "there's a problem", "i'm having trouble", "i'm struggling with", "i'm dealing with", "i don't know how to", "i can't figure out", "i'm going through", "i'm facing"]
    
    # Personal stories
    personal_stories = ["let me tell you", "i want to share", "i've never told", "this happened to me", "my experience", "my story", "when i was", "i remember", "i went through", "my life has been", "so basically", "long story short"]
    
    # Seeking understanding
    seeking_understanding = ["does that make sense", "you know what i mean", "do you understand", "am i clear", "can you understand", "if that makes sense", "i'm trying to explain", "ya know", "idk if that makes sense", "yk what i mean"]
    
    # Detailed reflections
    detailed_reflections = ["i've been thinking", "i've realized", "i've noticed", "i've been wondering", "i've come to understand", "i've learned", "i've discovered", "it occurred to me", "been reflecting", "just realized"]
    
    # Expressions of deep feelings
    deep_feelings = ["i feel so deeply", "it hurts so much", "i'm in so much pain", "i've never felt this", "the pain is unbearable", "i can't take this feeling", "my heart is broken", "i feel empty inside", "i'm drowning in", "can't deal", "i'm at my limit"]
    
    # Check for each type in order of priority
    for phrase in greetings:
        if text.startswith(phrase):
            return "greeting"
    
    for phrase in how_are_you:
        if phrase in text:
            return "how_are_you"
    
    for phrase in feeling_questions:
        if phrase in text:
            return "feeling_question"
    
    for phrase in gratitude:
        if phrase in text:
            return "gratitude"
    
    for phrase in about_bot:
        if phrase in text:
            return "about_bot"
    
    for phrase in help_requests:
        if phrase in text:
            return "help_request"
    
    for phrase in problem_statements:
        if phrase in text:
            return "problem_statement"
    
    # New conversation types
    for phrase in personal_stories:
        if phrase in text:
            return "personal_experience"
    
    for phrase in seeking_understanding:
        if phrase in text:
            return "seeking_understanding"
    
    for phrase in detailed_reflections:
        if phrase in text:
            return "detailed_reflection"
    
    for phrase in deep_feelings:
        if phrase in text:
            return "deep_feelings"
    
    # Check for single word responses
    if len(text.split()) <= 2:
        # Handle yes/no or very short responses
        if text in ["yes", "yeah", "yep", "yup", "sure", "ok", "okay", "y", "ye", "yh", "ya"]:
            return "agreement"
        elif text in ["no", "nope", "nah", "n", "nuh uh", "naur"]:
            return "disagreement"
        elif text in ["why", "how", "what", "when", "where", "who", "wdym", "wym", "huh", "???"]:
            return "question"
        elif text in ["good", "bad", "sad", "happy", "angry", "tired", "fine", "great", "terrible", "meh", "oof", "bleh"]:
            return "mood_statement"
    
    return None

# Extract names from conversation
def extract_names(text):
    # Simple name extraction using common patterns
    name_patterns = [
        r"(?:I'm|I am|this is|call me|name is) ([A-Z][a-z]+)",
        r"(?:my name'?s) ([A-Z][a-z]+)"
    ]
    
    for pattern in name_patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]
    
    return None

# Extract emotions from text with more nuanced detection
def extract_emotions(text):
    text = text.lower()
    emotions = {
        "happy": ["happy", "glad", "joy", "excited", "great", "good", "wonderful", "fantastic", "amazing", "delighted", "pleased", "cheerful", "content", "thrilled", "ecstatic", "love", "smile", "laugh", "enjoy", "fun", "bright", "positive", "blessed"],
        "sad": ["sad", "unhappy", "depressed", "down", "blue", "miserable", "heartbroken", "gloomy", "disappointed", "upset", "disheartened", "grief", "sorrow", "tearful", "hurt", "broken", "despair", "devastated", "empty", "lost", "alone", "lonely", "abandoned"],
        "angry": ["angry", "mad", "furious", "annoyed", "irritated", "frustrated", "rage", "outraged", "pissed", "resentful", "hostile", "bitter", "enraged", "hate", "fury", "disgusted", "contempt", "dislike", "aversion", "fed up"],
        "anxious": ["anxious", "nervous", "worried", "scared", "afraid", "fearful", "terrified", "panicked", "uneasy", "tense", "apprehensive", "stressed", "restless", "jittery", "on edge", "overwhelmed", "freaked out", "dread", "panic", "fretful", "troubled", "concerned"],
        "neutral": ["okay", "fine", "alright", "neutral", "so-so", "meh", "indifferent", "neither", "average", "middle", "normal", "usual"],
        "confused": ["confused", "puzzled", "perplexed", "unsure", "uncertain", "don't understand", "lost", "disoriented", "bewildered", "unclear", "ambivalent", "mixed feelings"],
        "hopeful": ["hopeful", "optimistic", "encouraged", "confident", "looking forward", "positive", "promising", "hopeful", "expect", "anticipate", "believe", "trust"],
        "tired": ["tired", "exhausted", "weary", "fatigued", "drained", "spent", "sleepy", "worn out", "burned out", "lethargic"],
        "grateful": ["grateful", "thankful", "appreciative", "blessed", "fortunate", "appreciate"]
    }
    
    # Enhanced emotion detection - check word proximity to better understand context
    words = text.split()
    found_emotions = []
    negation_words = ["not", "don't", "doesn't", "didn't", "isn't", "aren't", "can't", "cannot", "never", "no"]
    
    # First check for direct emotion mentions
    for emotion, keywords in emotions.items():
        # Look for emotions with context to avoid false positives
        for keyword in keywords:
            if keyword in words:
                # Check for negations (e.g., "not happy")
                idx = words.index(keyword)
                if idx > 0 and words[idx-1] in negation_words:
                    # If negated, don't add this emotion
                    continue
                # Otherwise add the emotion
                found_emotions.append(emotion)
                break
    
    # Special case for "I feel" or "feeling" statements which are strong indicators
    feel_idx = -1
    if "feel" in words:
        feel_idx = words.index("feel")
    elif "feeling" in words:
        feel_idx = words.index("feeling")
    
    if feel_idx >= 0 and feel_idx < len(words) - 1:
        # Check words after "feel"/"feeling"
        for emotion, keywords in emotions.items():
            if words[feel_idx + 1] in keywords:
                if emotion not in found_emotions:
                    found_emotions.append(emotion)
    
    # If no emotions detected, return neutral
    return found_emotions if found_emotions else ["neutral"]

# Enhanced predefined responses with more variations and reflective listening
RESPONSES = {
    "greeting": [
        "Hello! I'm here to provide support. How are you feeling today?",
        "Hi there. I'm your mental health support assistant. How can I help you today?",
        "Welcome. I'm here to listen and provide support. What's on your mind?",
        "Hello! I'm here to chat about what's going on in your life. How are you feeling?",
        "Hello and welcome. This is a safe space to share whatever you're going through. How are you today?",
        "Hi there. I'm here to listen without judgment. What would you like to talk about today?"
    ],
    "greeting_casual": [
        "Hey! Nice to meet you. How's everything going?",
        "Hi there! What's on your mind today?",
        "Hey! I'm here for you. What would you like to chat about?",
        "Hello! I'm all ears. How's your day been so far?",
        "Hey! What's up? I'm here whenever you need to talk.",
        "Hi there! How's life treating you lately?"
    ],
    "greeting_gen_z": [
        "Heyyy! What's good? How's your vibe today?",
        "Hi there! ✨ How's it going?",
        "Hey! Ready to chat whenever you are!",
        "Sup! How's your day treating you?",
        "Hey there! Tell me what's going on in your world rn",
        "Hi! I'm all ears for whatever you want to talk about!",
        "Hey! Spill the tea - how's life lately?",
        "Hi friend! What's on your mind today?"
    ],
    "greeting_with_name": [
        "Hello {name}! It's nice to see you. How are you feeling today?",
        "Hi {name}! I'm here to support you. What's on your mind?",
        "Welcome back, {name}. How have things been going since we last chatted?",
        "Good to see you, {name}! How can I help you today?",
        "Hello {name}! I've been looking forward to our conversation. What's been happening in your world?",
        "Hi {name}! It's great to connect with you again. How have you been since we last talked?"
    ],
    "how_are_you": [
        "Thanks for asking! I'm here and ready to support you. How about you? How have you been feeling lately?",
        "I'm here and focused on how I can help you today. What's been going on in your world?",
        "I'm doing well, thank you for asking. More importantly, how are you feeling today?",
        "I appreciate you asking. I'm here specifically to listen and support you. How have things been for you?"
    ],
    "feeling_question": [
        "I'm designed to be here for you, no matter what you're going through. How are you feeling today?",
        "Thanks for checking in. I'm here to focus on your well-being. What's been on your mind?",
        "I'm here and ready to listen. More importantly, how have you been feeling lately?",
        "I'm always here to chat with you. What kinds of feelings have you been experiencing recently?"
    ],
    "anxiety": [
        "It sounds like you might be experiencing some anxiety. Remember that deep breathing exercises can help calm your nervous system. Try breathing in for 4 counts, holding for 2, and exhaling for 6 counts.",
        "Feeling anxious can be challenging. Grounding techniques like the 5-4-3-2-1 method (notice 5 things you see, 4 things you feel, 3 things you hear, 2 things you smell, and 1 thing you taste) might help bring you to the present moment.",
        "Anxiety is a normal human emotion, but it can be overwhelming. Consider setting small, manageable goals for yourself today and celebrate when you accomplish them.",
        "When anxiety feels overwhelming, progressive muscle relaxation can help. Try tensing and then releasing each muscle group in your body, starting from your toes and working up to your head."
    ],
    "depression": [
        "I hear that you're feeling down. Remember that small steps matter - even getting out of bed or taking a shower is an achievement when you're feeling depressed.",
        "Depression can make everything feel more difficult. Try to be gentle with yourself, the way you would with a good friend going through a tough time.",
        "When feeling low, it can help to connect with others, even though that might be the last thing you feel like doing. Consider reaching out to someone you trust.",
        "Creating a routine can provide structure when you're feeling depressed. Even simple activities like going for a short walk each day can help improve your mood over time."
    ],
    "stress": [
        "Managing stress is important for your wellbeing. Consider what aspects of the situation you can control and which you cannot, then focus your energy on the things within your control.",
        "When feeling stressed, taking short breaks throughout your day to reset can be helpful. Even 5 minutes of mindfulness or stretching can make a difference.",
        "Stress often builds up when we don't make time for self-care. What activities help you relax? Can you incorporate more of these into your routine?",
        "Setting boundaries is essential for managing stress. It's okay to say no to additional responsibilities when you're already feeling overwhelmed."
    ],
    "sleep": [
        "Sleep difficulties can significantly impact mental health. Establishing a consistent bedtime routine might help signal to your body that it's time to wind down.",
        "If racing thoughts keep you awake, try jotting them down in a journal before bed to help clear your mind.",
        "Limiting screen time before bed and creating a cool, dark, quiet sleeping environment can help improve sleep quality.",
        "Relaxation techniques like progressive muscle relaxation or guided imagery might help you fall asleep more easily."
    ],
    "relationship": [
        "Relationship challenges can be very stressful. Clear communication about your feelings and needs is often helpful, using 'I' statements rather than accusations.",
        "In relationships, it's important to recognize that you can only control your own actions and responses, not those of others.",
        "Taking time for yourself is important even in close relationships. Maintaining your own interests and friendships helps create a healthy balance.",
        "Conflict in relationships is normal, but how we handle it matters. Try to approach disagreements with curiosity rather than defensiveness."
    ],
    "work": [
        "Work stress can feel overwhelming. Setting clear boundaries between work and personal time can help maintain balance.",
        "Breaking large work tasks into smaller, manageable steps can make them feel less daunting.",
        "Remember that your worth isn't defined by your productivity or work achievements. It's important to make time for rest and activities you enjoy.",
        "If workplace issues are affecting your mental health, consider what changes might improve the situation - whether that's discussing concerns with your manager, adjusting your work environment, or exploring other opportunities."
    ],
    "trauma": [
        "I hear you mentioning some potentially traumatic experiences. Remember that healing from trauma takes time, and it's okay to progress at your own pace.",
        "When dealing with trauma, having a strong support system can be invaluable. Is there someone you trust who you could talk to about these experiences?",
        "Trauma can affect us in many ways. Grounding techniques may help when memories feel overwhelming. One approach is to focus on your five senses to bring yourself back to the present moment.",
        "It takes courage to talk about difficult experiences. If you're struggling with trauma, working with a professional who specializes in trauma-informed care can be very helpful."
    ],
    "family": [
        "Family relationships can be complex. It sounds like you're navigating some challenges there. What aspects feel most difficult right now?",
        "Our families often have a significant impact on our wellbeing. Setting healthy boundaries with family members can sometimes help manage difficult dynamics.",
        "It can be challenging when family situations are causing distress. Are there specific patterns or interactions that you find particularly difficult?",
        "Family relationships involve many emotions. It's okay to acknowledge both the positive feelings and the challenging ones."
    ],
    "general": [
        "Thank you for sharing. How long have you been feeling this way?",
        "It takes courage to talk about what you're experiencing. Would you like to tell me more about what's been happening?",
        "I appreciate you opening up. What are some things that have helped you cope with difficult feelings in the past?",
        "Your feelings are valid. Taking care of your mental health is important. What kind of support are you looking for today?"
    ],
    "followup": [
        "How have you been managing these feelings so far?",
        "What has helped you cope with similar situations in the past?",
        "Is there someone in your life you feel comfortable talking to about what you're experiencing?",
        "Would you find it helpful to explore some coping strategies that might work for your situation?",
        "Are there any small steps you feel you could take today that might help you feel a bit better?"
    ],
    "followup_casual": [
        "What's been on your mind lately?",
        "Anything specific you'd like to chat about today?",
        "How has your day been going so far?",
        "Is there something particular that's bothering you that you'd like to discuss?"
    ],
    "reflective": [
        "It sounds like you're feeling {emotion} about {topic}. Would you like to explore that further?",
        "I'm hearing that {topic} has been causing you to feel {emotion}. How long has this been going on?",
        "It seems like {topic} is really impacting you. How has this been affecting other areas of your life?",
        "From what you're sharing, {topic} is bringing up {emotion} feelings for you. What do you think might help in this situation?"
    ],
    "continue_topic": [
        "Earlier you mentioned {topic}. Would you like to talk more about that?",
        "I remember you brought up {topic} before. Has anything changed with that situation?",
        "You previously mentioned {topic}. How are you feeling about that now?",
        "Going back to what you said about {topic}, could you share more about how that's affecting you?"
    ],
    "validation": [
        "It makes complete sense that you would feel that way given what you're going through.",
        "Your feelings are valid. Many people would feel similarly in your situation.",
        "That sounds really challenging. It's understandable that you're feeling this way.",
        "I can hear how difficult this has been for you. Your reactions are completely normal."
    ],
    "gratitude": [
        "You're welcome. I'm glad I could be helpful.",
        "It's my pleasure to support you.",
        "I'm here for you anytime you need to talk.",
        "I appreciate your kind words. How else can I help you today?"
    ],
    "about_bot": [
        "I'm a mental health support chatbot designed to provide a listening ear and helpful resources. While I'm not a human therapist, I aim to offer supportive conversations and coping strategies. How can I assist you today?",
        "I'm an AI assistant focused on mental health support. I can listen, suggest coping strategies, and provide resources. Remember though, I'm not a replacement for professional help. What's on your mind?",
        "I'm here to provide mental health support through conversation and resources. While I'm not a human counselor, I'm designed to be a supportive presence. How are you feeling today?",
        "I'm a digital mental health companion, created to provide supportive conversations and helpful resources. I'm not a licensed therapist, but I can offer a space to talk and share coping strategies. How can I support you?"
    ],
    "help_request": [
        "I'm here to help. Could you tell me more about what you're going through so I can better understand how to support you?",
        "I'll do my best to help you. What specific challenges are you facing right now?",
        "I'm ready to support you. Can you share more about what kind of help you're looking for?",
        "I'm here to assist however I can. Let's explore what's going on and what might help."
    ],
    "agreement": [
        "I appreciate your agreement. Would you like to tell me more about your thoughts on this?",
        "Great. Is there something specific about this you'd like to explore further?",
        "Thank you for sharing. How does this make you feel?",
        "I hear you. What else is on your mind about this?"
    ],
    "disagreement": [
        "I understand you don't agree. Would you like to share your perspective?",
        "That's completely fine. Everyone's experience is different. Can you tell me more about your thoughts?",
        "I appreciate your honesty. What would feel more helpful to you?",
        "Thank you for letting me know. What approach would work better for you?"
    ],
    "question": [
        "That's a good question. Could you elaborate a bit more so I can better understand what you're asking?",
        "I'd be happy to explore that with you. Can you provide a bit more context about what you're wondering?",
        "Great question. To help me give you the most helpful response, could you share a little more about what's prompting this question?",
        "I'm glad you asked. Can you tell me more about what you're hoping to learn?"
    ],
    "mood_statement": [
        "Thank you for sharing how you're feeling. Would you like to talk more about what's contributing to that feeling?",
        "I appreciate you letting me know. How long have you been feeling this way?",
        "Thank you for sharing that with me. Is there something specific that's making you feel this way?",
        "I hear you. Would it be helpful to explore some strategies related to managing these feelings?"
    ],
    "direct_emotion": [
        "I hear that you're feeling {emotion} right now. That's completely valid - all emotions provide us with important information.",
        "Thank you for sharing that you're feeling {emotion}. I appreciate your openness about your emotions.",
        "It takes courage to acknowledge feeling {emotion}. Would you like to explore what might be contributing to this feeling?",
        "I'm sorry you're feeling {emotion} right now. Would it help to talk more about what's behind this emotion?"
    ],
    "problem_statement": [
        "I'm here for you. Please tell me more about what's going on so I can better understand how to support you.",
        "I'm listening. Could you share more details about what problem you're facing? I'm here to help.",
        "Thank you for reaching out. I'd like to understand more about what's happening. Can you tell me about the problem you're experiencing?",
        "I'm sorry to hear you're dealing with a problem. Would you feel comfortable sharing more about what's troubling you? I'm here to listen and support you."
    ],
    "crisis_support": [
        "I'm really concerned about what you're sharing. Your safety and wellbeing matter deeply. These thoughts can feel overwhelming, but you don't have to face them alone. There are trained professionals who can help during difficult moments like this. Would you be willing to reach out to a crisis helpline right now?",
        "I hear how much pain you're in right now. What you're feeling is real, but please know that these intense feelings can change with the right support. You deserve to be here and to receive help. Would it be possible for you to call a crisis line to talk with someone trained to help with these feelings?",
        "Thank you for trusting me with these thoughts. That shows incredible courage. These feelings can be terrifying, but they don't have to be faced alone. Please consider calling a crisis support line right now - they can offer immediate help and a safe space to talk through these feelings.",
        "I'm really sorry you're experiencing such deep pain. Your life has value, even if it might not feel that way right now. These thoughts are a signal that you need and deserve support. Would you be willing to reach out to a crisis counselor? They're available 24/7 and can help you navigate these difficult feelings."
    ],
    "hopelessness_support": [
        "I hear how exhausted and hopeless things feel right now. These heavy feelings are real, but they don't define you or your future. Even in the darkest moments, possibilities exist that can't be seen right now. Would you like to talk more about what's been happening that's led to these feelings?",
        "I'm truly sorry you're feeling this way. The weight of hopelessness can make everything seem impossible. But you've shown strength just by reaching out today. Sometimes when we can't see hope, we borrow it from others until we find our own again. What's been most difficult for you lately?",
        "That sounds incredibly heavy to carry. Feeling like nothing will improve can be so isolating, but you're not alone in this struggle. Every person has inherent worth—including you—regardless of what your mind might be telling you right now. Can you share what's contributed to feeling this way?",
        "I'm really sorry things feel so overwhelming. When we're in that dark place, it's almost impossible to imagine things changing. But your brain in pain doesn't always tell you the truth about your future. You matter, and your pain matters. Would you feel comfortable telling me more about what's going on?"
    ],
    "affirmations": [
        "Even on your darkest days, you still matter. Your presence in this world makes a difference in ways you might not even realize.",
        "You've made it through every difficult day so far—that shows incredible strength, even when you don't feel strong.",
        "Your worth isn't measured by your productivity, your mood, or your struggles. You have inherent value simply by being you.",
        "This moment doesn't define your entire future. Things can and do change, even when it feels impossible.",
        "The fact that you're reaching out shows remarkable courage. It takes strength to be vulnerable about these feelings.",
        "You deserve compassion and understanding, especially from yourself. Please be as gentle with yourself as you would be with someone you love.",
        "Your feelings are valid, but they're not permanent. With support and time, these intense feelings can shift.",
        "You are not a burden. The people who care about you want to support you through difficult times.",
        "You don't have to face these feelings alone. Reaching out for help is a sign of strength, not weakness.",
        "You've navigated difficult times before, and that resilience is still within you, even if you can't feel it right now."
    ],
    "violent_thoughts_critical": [
        "I notice you're expressing some really intense feelings about hurting someone. Those are serious thoughts, and I want to acknowledge the pain or anger you must be feeling right now. However, I need to emphasize that acting on these thoughts can have severe consequences. Would you be willing to talk to a professional who can help you process these feelings in a healthier way?",
        "I can hear that you're in a very difficult place emotionally. The intensity of these feelings must be overwhelming. While anger is completely valid, acting on thoughts of harming others is not a solution and can lead to irreversible consequences. A mental health professional would be better equipped to help you navigate these intense emotions. Would you consider reaching out to one?",
        "That's a really powerful emotion you're expressing. I can tell something significant has happened to make you feel this way. Your feelings matter and deserve attention, but I'm concerned about the potential for harm. Can we talk about what's driving these feelings and explore healthier ways to address the situation?",
        "I understand you're feeling intense anger right now. Those feelings are valid, but acting on thoughts of harming others is never the solution and can have devastating consequences for everyone involved. Would it help to talk about what's behind these feelings and explore ways to manage them safely?"
    ],
    "violent_thoughts_venting": [
        "It sounds like you're carrying a tremendous amount of anger right now. That's a really powerful emotion, and it often comes from a place of hurt or injustice. Would you like to talk more about what's happening that's brought you to this point? We might be able to find healthier ways to process these feelings.",
        "I hear how angry you are. Anger like this often masks deeper feelings like hurt, betrayal, or powerlessness. While it's important to acknowledge these feelings, it's equally important to find safe ways to express them. What do you think might be underneath this anger?",
        "That's a lot of intense emotion you're expressing. Sometimes when we feel this level of rage, it's because a boundary has been crossed or a core need isn't being met. Can you tell me more about what happened? Understanding the source might help us find better ways to address it.",
        "I'm hearing a lot of rage in what you're saying. Anger is often a secondary emotion that protects us from more vulnerable feelings like hurt or fear. Would you be willing to explore what might be beneath this anger? There are healthier ways to process these emotions that won't lead to regret later."
    ],
    "violent_thoughts_processing": [
        "Thank you for being open about these difficult feelings. When we experience intense anger, our bodies actually go into fight-or-flight mode, which can cloud our judgment. Let's try to understand what's happening and find healthier ways to address it. Can you tell me more about the situation that triggered these thoughts?",
        "I appreciate your honesty about these feelings. Intense anger can sometimes feel like it needs an outlet, but there are ways to process it without causing harm. Would it help to explore some techniques for managing these powerful emotions in the moment?",
        "Those are really powerful feelings you're describing. It takes courage to acknowledge them. Our brains can sometimes go to extreme places when we're hurt or threatened. Can we talk about what happened and explore some healthier ways to respond to this situation?",
        "I understand you're feeling overwhelmed with these thoughts. When we're flooded with anger, our thinking can become black and white. Let's work on bringing some balance back. What specific situation or interaction has triggered these intense feelings?"
    ],
    "safety_resources": [
        """
        **If you're experiencing thoughts of harming others:**
        
        - National Crisis Hotline: Call or text 988
        - Trevor Project (LGBTQ+): 1-866-488-7386
        - Crisis Text Line: Text HOME to 741741
        
        These services are confidential and available 24/7 with trained counselors who can help during difficult moments.
        
        Remember: Strong emotions are temporary, but actions can have permanent consequences.
        """
    ],
    "personal_experience": [
        "Thank you for sharing that experience with me. Personal stories can be difficult to share, and I appreciate your trust.",
        "That sounds like a significant experience in your life. Would you like to explore how it's shaped who you are today?",
        "I appreciate you opening up about that experience. How do you feel it's impacted your current situation?",
        "Thank you for trusting me with that story. Would it help to talk about how those experiences connect to what you're feeling now?",
        "That's a powerful story from your life. Have you been able to process these experiences with anyone else?"
    ],
    
    "childhood_trauma": [
        "Childhood experiences can have profound impacts on us. Thank you for sharing something so personal.",
        "Early life experiences shape so much of how we see the world. I hear how difficult that was for you.",
        "Growing up in those circumstances sounds incredibly challenging. How do you feel it affects you today?",
        "Thank you for sharing about your childhood. Those early experiences can leave lasting impressions on how we relate to ourselves and others.",
        "I'm truly sorry you went through that as a child. No child should have to experience that kind of pain."
    ],
    
    "relationship_loss": [
        "Losing someone important, whether through a breakup, death, or distance, can be deeply painful. I'm sorry you're experiencing this loss.",
        "Relationship endings can leave us feeling like a part of ourselves is missing. Your grief is completely valid.",
        "The pain of losing someone significant is very real. How have you been coping with these feelings of loss?",
        "I hear how much this relationship meant to you. Would it help to talk more about the specific aspects you're missing?",
        "That kind of relationship loss can feel overwhelming. Please be gentle with yourself as you navigate through this."
    ],
    
    "identity_struggle": [
        "Questioning aspects of your identity is a profound journey. Whatever you discover, your feelings are valid.",
        "Exploring who you truly are takes courage. I'm here to support you through this process of self-discovery.",
        "Identity questions touch the core of who we are. It makes sense that this feels both important and challenging.",
        "Thank you for sharing this part of your journey with me. How long have you been exploring these questions about yourself?",
        "The path to understanding yourself can sometimes feel uncertain. What aspects have been most challenging for you?"
    ],
    
    "life_transition": [
        "Major life transitions can shake our sense of stability. It's normal to feel uncertain during these times of change.",
        "Changes like these often bring mixed emotions - excitement, anxiety, grief, hope. All of these feelings are valid.",
        "Navigating a significant life transition takes real strength. How are you taking care of yourself during this time?",
        "This sounds like a meaningful turning point in your life. What aspects of this change feel most challenging?",
        "Times of transition can reveal our resilience. I hear that you're dealing with a lot of change right now."
    ],
    
    "validation_deep": [
        "What you're experiencing is profound and real. Your pain matters, and so do you.",
        "I want you to know that your struggle is legitimate. These feelings, no matter how overwhelming, are part of your human experience.",
        "Your suffering is valid. Full stop. You don't need to justify or minimize what you're going through.",
        "I believe you. I hear you. Your experience is real and significant.",
        "The depth of what you're feeling makes complete sense given what you've been through. Anyone would struggle with this."
    ],
    
    "affirmations_extended": [
        "Your willingness to look within shows tremendous courage. That inner strength will help guide you through this.",
        "Even in moments when you can't see your own worth, it remains constant. You matter, unconditionally.",
        "Growth isn't linear - your 'setbacks' are actually valuable information on your healing journey.",
        "The fact that you're reaching out shows remarkable self-awareness and courage.",
        "You've survived every difficult day so far - that's evidence of an inner strength that's always with you.",
        "Your ability to articulate these difficult feelings shows remarkable emotional intelligence."
    ],
    
    "relationship_concern": [
        "Relationship dynamics can be really challenging. Would you like to explore what patterns might be happening here?",
        "I hear you're struggling with this relationship. These situations often have complex emotions on both sides. What do you think is at the core of what's happening?",
        "Relationships require vulnerability and trust, which makes them both rewarding and difficult. How has this been affecting you?",
        "That sounds like a painful relationship situation. Would it help to talk about what healthy boundaries might look like here?"
    ],
    
    "relationship_pattern": [
        "Our relationship patterns often have roots in our earliest attachments. Would it help to explore what feels familiar about this situation?",
        "Sometimes we repeat relationship patterns until we heal the underlying needs. What patterns have you noticed in your relationships?",
        "The people we're drawn to can tell us a lot about our unmet needs and past experiences. Have you noticed any similarities in your relationships?",
        "Breaking recurring relationship patterns starts with awareness. You're already showing courage by reflecting on this."
    ],
    
    "relationship_loss": [
        "Losing a connection with someone, whether through breakup, distance, or conflict, can feel like grieving. How are you taking care of yourself through this?",
        "The end of a relationship can leave a space that feels impossible to fill. It's okay to mourn that loss and also to know that healing is possible.",
        "That kind of rejection or disconnection can be deeply painful. Your feelings about this are completely valid.",
        "Relationship endings often bring up complex emotions - sadness, anger, relief, confusion. All of these feelings deserve space and acknowledgment."
    ],
    
    "relationship_trust": [
        "Trust is fragile and rebuilding it takes time. What small steps might feel safe to you right now?",
        "When trust has been broken, it's natural to feel hesitant about being vulnerable again. Your caution is protecting you.",
        "Trust is built in small moments of reliability over time. It might help to look for those small consistent actions rather than grand gestures.",
        "Learning to trust again often means balancing healthy caution with openness. It's okay to move at your own pace with this."
    ],
    
    "relationship_boundary": [
        "Setting boundaries is about honoring your needs and values. What boundaries do you think might be missing in this situation?",
        "It can be challenging to maintain boundaries, especially with people we care about. What makes it difficult for you to set limits?",
        "Healthy relationships respect each person's boundaries. How might you communicate your needs more clearly?",
        "Boundaries aren't about pushing people away - they're about teaching others how to treat you with respect. What boundary would help you feel safer?"
    ],
    
    "heartbreak": [
        "That kind of pain hits deep. Heartbreak isn't just emotional—it's physical too. Your body remembers connection. Would you like to talk about what you miss most?",
        "Heartbreak creates a special kind of silence in your life. The absence of someone who once filled your days. I'm here to listen if you want to share more about what you're feeling.",
        "When someone leaves, they take pieces of your shared world with them. It's okay to grieve those lost futures and possibilities. What feels hardest right now?",
        "That ache of missing someone can feel bottomless sometimes. You don't have to navigate it alone. What's been most difficult for you in this process?"
    ],
    
    "breakup_ghosting": [
        "Being left without closure or explanation can feel like a special kind of betrayal. That silence often hurts more than words would. What would you say to them if you had the chance?",
        "Ghosting leaves you holding all the pieces, trying to make sense of what happened. That uncertainty can be harder than a clear ending. How have you been trying to find closure?",
        "When someone disappears without explanation, it's natural to fill that silence with self-doubt. But their leaving says more about them than about you. What thoughts have been heaviest for you?",
        "That kind of disappearance leaves you questioning everything—including your own perceptions. I want you to know that your feelings are valid, even without their confirmation. What has been hardest to process?"
    ],
    
    "betrayal": [
        "Betrayal cuts deep because it breaks trust at its foundation. What you're feeling—the hurt, anger, confusion—it's all valid. Would you like to talk about what happened?",
        "When trust is broken, it can shake your sense of reality and make you question your judgment. That's a normal response to betrayal, not a flaw in you. How has this affected your ability to trust?",
        "The pain of betrayal often comes in waves—sometimes it's anger, sometimes deep sadness, sometimes questioning yourself. All those feelings deserve space. Where do you find yourself most often?",
        "Healing from betrayal takes time because you're not just grieving the relationship, but also the version of it you believed in. That's a complex loss. What feelings come up strongest for you right now?"
    ],
    
    "breakup_still_love": [
        "Loving someone even after the relationship ends is such a human experience. Love doesn't always follow the same timeline as relationships. What aspects of them do you find hardest to let go of?",
        "It's possible to both love someone and recognize that the relationship wasn't right. That contradiction can be painful to hold. How are you navigating those complicated feelings?",
        "Love fades slower than pain sometimes. That doesn't mean you made a mistake in loving them—it means your capacity for connection is deep. How are you caring for yourself while these feelings are still present?",
        "The heart doesn't always follow logic. You can know something is over while still feeling deeply attached. Both realities can exist at once. What helps you when those feelings of love feel overwhelming?"
    ],
    
    "breakup_comparison": [
        "Seeing them move on or appear happy can trigger so much pain and questioning. Remember that social media and appearances rarely tell the full story. What specific feelings come up when you see them now?",
        "Comparing your healing journey to theirs is a natural impulse, but healing isn't linear or competitive. Your process is your own. What would help you focus on your path rather than theirs?",
        "It can feel like a special kind of pain when they seem to have moved on faster. But appearing 'fine' doesn't always mean they've processed everything. What would genuine healing look like for you?",
        "That contrast between their apparent happiness and your pain can feel cruel. But your healing isn't dependent on their timeline. What small steps could help you reclaim your joy?"
    ],
    
    "breakup_moving_on": [
        "The question of when you'll feel better is so common after heartbreak. Healing doesn't usually happen all at once—it comes in moments of reprieve that gradually grow longer. What small moments of peace have you noticed?",
        "Moving on doesn't mean forgetting or never feeling pain about what happened. It means the pain becomes part of your story, not your whole story. What would a meaningful next chapter look like for you?",
        "Finding yourself again after a relationship ends can be both frightening and freeing. There's space now to rediscover parts of yourself that may have been set aside. What aspects of yourself are you curious to explore?",
        "Building a life after significant loss takes courage. Every small step toward your own well-being matters. What's one tiny thing that has brought you comfort or joy recently?"
    ],
    
    "bad_day": [
        "I'm sorry to hear you're having a rough day. Would you like to talk about what happened? Sometimes unpacking it can help lighten the load.",
        "Ugh, those days when nothing seems to go right are so draining. What was the most frustrating part of your day?",
        "It sounds like today has been really challenging. I'm here to listen if you want to vent or just talk through it.",
        "Bad days can really wear you down. Is there anything specific that's bothering you the most right now?",
        "Those days that just hit different... I hear you. What felt particularly off about today?",
        "Days like that can be so heavy. Is there something specific that triggered these feelings, or has it been building up?",
        "I'm sorry your day wasn't what you hoped for. Sometimes talking it through can help process those feelings. What's on your mind?",
        "It sounds like you've been carrying a lot today. Want to share what's been weighing on you?"
    ],
    
    "feeling_invisible": [
        "That feeling of invisibility can be so painful - like you're shouting into a void. I want you to know that I see you. Would you like to share more about what's making you feel this way?",
        "Feeling unseen or unheard is really difficult. I'm here and I'm listening. What's been happening that's made you feel invisible?",
        "It can be so isolating when you feel like no one notices you. I notice you. Would you like to talk about what's been going on?",
        "That sense that no one sees your efforts or your struggles - it's really painful. I'd like to understand more about your experience if you're willing to share."
    ],
    
    "feeling_overwhelmed": [
        "When everything piles up, it can feel impossible to even know where to start. What's feeling most urgent or heavy for you right now?",
        "That overwhelmed feeling can be so paralyzing. Let's try to break it down into smaller pieces. What's one thing that's contributing to this feeling?",
        "I hear that you're feeling swamped right now. Sometimes naming the specific things that are overwhelming us can help. Would you like to try that?",
        "It sounds like you've got a lot on your plate. Would it help to talk through what's specifically feeling like too much right now?"
    ],
    
    "self_criticism": [
        "It sounds like you're being really hard on yourself. We all make mistakes, but that doesn't define your worth. Would you talk to a friend the way you're talking to yourself?",
        "That inner critic can be so harsh. What if we try to approach this with a bit more gentleness? What would a compassionate view of the situation look like?",
        "I notice you're taking a lot of responsibility for things that might not be entirely in your control. Could we explore that a bit more?",
        "It's so easy to blame ourselves when things don't go as planned. But often, there are many factors involved. What else might have contributed to what happened?"
    ],
    
    "feeling_misunderstood": [
        "Feeling misunderstood can be really isolating. I'm here to listen without judgment. What do you wish people understood about you?",
        "It's hard when it feels like no one gets you. I'd like to understand better - could you share more about what feels misunderstood?",
        "That disconnect between how you feel and how others perceive you can be really frustrating. What would help you feel more seen and understood?",
        "I hear that you're feeling like people don't get you. That's a lonely feeling. What aspect of yourself or your experience do you wish others could see more clearly?"
    ],
    
    "emotional_exhaustion": [
        "Emotional exhaustion is real and valid. Sometimes we need to just acknowledge how tired we are before we can start to recover. What has been draining you lately?",
        "Being emotionally drained can feel like there's nothing left to give - to yourself or others. What small thing might help you recharge, even just a little?",
        "That kind of deep tiredness goes beyond just needing sleep. It sounds like you need some genuine restoration. What has helped you refill your emotional cup in the past?",
        "When we're emotionally exhausted, even small tasks can feel overwhelming. Is there something specific that feels particularly hard right now?"
    ],
    
    "grief_loss": [
        "I'm so sorry for your loss. Grief is as unique as your relationship with the person you lost. Would you like to share more about them?",
        "The pain of loss can feel overwhelming. There's no right way to grieve, and no timeline for healing. How are you coping day to day?",
        "Losing someone you love leaves a space that nothing can quite fill. What has been the hardest part for you recently?",
        "Grief can come in waves, sometimes when we least expect it. Know that whatever you're feeling is a natural part of the process."
    ],
    "identity_confusion": [
        "Questioning who you are can be both unsettling and an opportunity for growth. What parts of yourself feel most authentic to you?",
        "Our sense of identity can shift through different life stages and experiences. What core values have remained consistent for you?",
        "Sometimes feeling lost in your identity comes after significant changes or losses. Has something shifted recently in your life?",
        "Reconnecting with yourself can start with simple questions like what you enjoy, what matters to you, and who you feel most yourself around. Would exploring these help?"
    ],
    "followup_gen_z": [
        "What's been on your mind lately?",
        "Anything specific you wanna chat about today?",
        "How's your day been going so far?",
        "Something specific bothering you rn?",
        "Wanna talk more about that?",
        "How've you been handling all this?",
        "What's your take on all this?",
        "Has anyone else noticed what you're going through?",
        "What would help you feel better rn?",
        "Have you tried any ways to deal with this already?"
    ],
    "help_request_gen_z": [
        "I got you! What's going on?",
        "I'm here for you! What's up?",
        "Ready to help! What's happening?",
        "I'm all ears - what do you need help with?",
        "Let's figure this out together. What's on your mind?",
        "I'm with you on this. What's going on?"
    ],
    "depression_gen_z": [
        "That feeling of emptiness is real tough. Your brain chemistry isn't just 'being dramatic' - depression is an actual health issue.",
        "It's so hard when your brain feels foggy and everything seems pointless. Depression can make even small tasks feel impossible.",
        "When you feel super low, just remember your brain is literally telling you lies. Depression does that - it's not the real you.",
        "That heavy feeling is so draining. Depression isn't just being sad - it's like your brain's battery is constantly low."
    ],
    "anxiety_gen_z": [
        "That anxious feeling is the worst. Your body's alarm system is basically glitching and going off when there's no real danger.",
        "When your thoughts start spiraling, it's like your brain's stuck in a toxic group chat it can't leave.",
        "Anxiety is like having too many tabs open in your brain all the time. It's exhausting.",
        "That constant worry is your brain being an overprotective parent. It means well but needs to chill sometimes."
    ],
    "validation_gen_z": [
        "That's completely valid. Anyone would feel the same way.",
        "You're not overreacting AT ALL. This is a lot to handle.",
        "That's so real. What you're feeling makes total sense.",
        "You're allowed to feel this way. Your emotions are 100% valid.",
        "That's a whole mood. Anyone would feel that way in your shoes."
    ],
    "affirmations_gen_z": [
        "You're stronger than you realize. Seriously.",
        "You've got this. It might not feel like it rn, but you do.",
        "Not to be dramatic, but you're literally doing amazing just by talking about this.",
        "The fact that you're still trying says a lot about your strength. That's iconic behavior.",
        "Just showing up today is a win. Give yourself credit for that.",
        "Your feelings are valid, your struggles are real, and you deserve support. Period."
    ],
    "general_solutions": [
        "I understand what you're going through. Here's something that might help: First, try to identify the specific aspects that are most challenging for you right now. Then, consider breaking those challenges into smaller, more manageable steps. Many people find that tackling one small piece at a time makes progress feel more achievable. Remember that it's also important to celebrate your small victories along the way.",
        
        "That sounds really difficult. One approach that has helped many people is to practice mindful awareness of your thoughts and feelings without judgment. Notice them as they arise, acknowledge them, and then gently bring your focus back to the present moment. This can create some emotional space between you and your challenges, making them feel less overwhelming.",
        
        "I hear you, and I want you to know your feelings are completely valid. Sometimes when we're struggling, it can help to use the RAIN technique: Recognize what you're feeling, Allow the experience to be there, Investigate with kindness where this feeling lives in your body, and Nurture yourself with compassion. This approach combines mindfulness with self-compassion in a way that many find healing.",
        
        "What you're experiencing is challenging, and I appreciate you sharing it. Something that might be worth trying is establishing a daily routine that includes activities that support your mental well-being - like a short morning walk, moments of mindful breathing throughout the day, and a wind-down ritual before bed. These structured habits can provide stability when everything else feels uncertain.",
        
        "That's a lot to deal with. One technique that combines cognitive and emotional approaches is journaling. Try writing down your thoughts for just 10 minutes a day, focusing particularly on identifying negative thought patterns and gently challenging them with more balanced perspectives. Many find this helps externalize their inner dialogue and see solutions more clearly.",
        
        "I'm sorry you're going through this. Something that has helped others in similar situations is the practice of 'opposite action' - when you feel an overwhelming emotion urging you to act in a certain way (like isolating when sad), try doing the opposite (reaching out to a friend) instead. This behavioral approach can sometimes help break difficult emotional cycles.",
        
        "What you're describing sounds really tough. One approach worth considering is the 5-5-5 rule for worries: Ask yourself if this will matter in 5 minutes, 5 months, or 5 years. This perspective shift can help calibrate your emotional response and focus your energy on the things that truly deserve your attention right now.",
        
        "I hear the struggle in what you're sharing. Something that combines multiple therapeutic approaches is creating a personalized coping toolkit - identify 5-7 strategies that have helped you in the past (like deep breathing, calling a friend, taking a walk, listening to specific music) and write them down somewhere accessible. When you're struggling, having these pre-identified options can make self-care decisions easier."
    ]
}

# Update RESPONSES with Earkick style responses
RESPONSES.update(EARKICK_RESPONSES)

# Add more diverse response templates for common categories
# Expand the greeting variations for Gen Z
if "greeting_gen_z" in RESPONSES:
    RESPONSES["greeting_gen_z"].extend([
        "Hey there! How's life treating you?",
        "What's poppin? How's your day going?",
        "Hi! Ready to chat about whatever's on your mind!",
        "Welcome back! Tell me what's new with you.",
        "Hey friend! How are you vibing today?",
        "What's good? How's everything going?",
        "Hey! I'm here to chat. What's up?",
        "Sup! What's on your mind today?"
    ])

# Add more casual followup questions for variety
if "followup_casual" in RESPONSES:
    RESPONSES["followup_casual"].extend([
        "What's been keeping you busy lately?",
        "Anything interesting happen recently?",
        "What's something you've been thinking about?",
        "How's life been treating you?",
        "Any highlights from your day so far?",
        "Something specific on your mind today?",
        "Anything you want to talk through?",
        "What's something that caught your attention lately?"
    ])

# Add more Gen Z style followups
if "followup_gen_z" in RESPONSES:
    RESPONSES["followup_gen_z"].extend([
        "What's been living in your head rent-free lately?",
        "Any tea you want to spill today?",
        "Vibes check - how's your energy today?",
        "What's your current mood? Main character energy or villain era?",
        "Anything making you stressed or anxious rn?",
        "What's something that hit different for you lately?",
        "Any wins you want to share? Big or small?",
        "What's your brain been fixating on lately?",
        "Anything you're lowkey worried about?",
        "What's giving you life these days?"
    ])
else:
    RESPONSES["followup_gen_z"] = [
        "What's been living in your head rent-free lately?",
        "Any tea you want to spill today?",
        "Vibes check - how's your energy today?",
        "What's your current mood? Main character energy or villain era?",
        "Anything making you stressed or anxious rn?",
        "What's something that hit different for you lately?",
        "Any wins you want to share? Big or small?",
        "What's your brain been fixating on lately?",
        "Anything you're lowkey worried about?",
        "What's giving you life these days?"
    ]

# Add general validation responses for more variety
if "validation" in RESPONSES:
    RESPONSES["validation"].extend([
        "What you're feeling makes a lot of sense given what you're going through.",
        "It's completely normal to feel that way in your situation.",
        "Many people would have similar reactions to what you're experiencing.",
        "Your feelings are a natural response to what's happening.",
        "It sounds like you're having a really tough time, and that's completely understandable.",
        "Those feelings are valid responses to challenging situations.",
        "I can see how difficult this is for you, and your reaction is completely natural.",
        "It's okay to feel this way - your emotions are giving you important information."
    ])

# Add varied responses for different emotional states
if "direct_emotion" in RESPONSES:
    RESPONSES["direct_emotion"].extend([
        "I can see that you're feeling {emotion} right now. Would you like to talk more about what's behind that feeling?",
        "When you say you're feeling {emotion}, what does that feel like for you specifically?",
        "I'm hearing that you're {emotion}. What do you think triggered that feeling?",
        "Being {emotion} can be really challenging. What helps you when you feel this way?",
        "I notice you're feeling {emotion}. How long have you been experiencing this?",
        "It sounds like you're feeling {emotion} right now. Is there a particular situation related to this feeling?",
        "I understand you're feeling {emotion}. What would be helpful for you right now?",
        "That {emotion} feeling you're describing makes a lot of sense given what you're going through."
    ])

# Add more diverse responses for problem statements
if "problem_statement" in RESPONSES:
    RESPONSES["problem_statement"].extend([
        "Thank you for sharing this challenge with me. Let's explore it together and see what might help.",
        "That sounds difficult to deal with. Can you tell me more about what's happening?",
        "I appreciate you opening up about this problem. What part of it is most concerning for you?",
        "I'm here to help you work through this. What have you already tried?",
        "Let's think about this together. What would a good outcome look like for you?",
        "This is clearly something important to you. How long has this been a concern?",
        "That's a challenging situation. What aspect would you like to focus on first?",
        "Thank you for trusting me with this. What do you think might be a first step toward addressing it?"
    ])

# Add more diverse help request responses
if "help_request" in RESPONSES:
    RESPONSES["help_request"].extend([
        "I'm listening and I want to help. Can you tell me more about what's going on?",
        "I'm here to support you. What kind of help would be most useful right now?",
        "I'll do my best to assist you. Let's talk about what you're experiencing.",
        "I appreciate you reaching out. What's been most on your mind lately?",
        "I'm glad you asked for help. That takes courage. What's happening that you need support with?",
        "I'm here for you. Let's figure this out together. Can you share more details?",
        "I want to help in the best way possible. What are you hoping we can accomplish today?",
        "Thank you for trusting me to help. What would be most supportive for you right now?"
    ])

# Add more diverse agreement responses
if "agreement" in RESPONSES:
    RESPONSES["agreement"].extend([
        "I'm glad we're on the same page. What else are you thinking about this?",
        "Thanks for confirming. Is there anything else you'd like to add?",
        "Great! Let's continue exploring this topic. What else feels important to discuss?",
        "I'm glad that resonates with you. Where would you like to take the conversation next?",
        "That's good to hear. Is there anything specific about this you'd like to focus on?",
        "I'm glad we're aligned on this. What other thoughts are you having?",
        "Thanks for sharing your perspective. Is there more you'd like to explore about this?",
        "I appreciate your input. What else is on your mind about this topic?"
    ])

# Add more diverse responses for general topics
if "general" in RESPONSES:
    RESPONSES["general"].extend([
        "Thank you for sharing this with me. What aspects of this situation are most important to you?",
        "I appreciate you opening up about this. How has this been affecting your day-to-day life?",
        "This sounds meaningful to you. What would be helpful to explore further?",
        "Thanks for bringing this up. What would be most supportive for you right now?",
        "I'm listening and I hear you. What would you like to focus on about this?",
        "Thank you for trusting me with this. How have you been managing so far?",
        "I'm here to listen and support you with this. What would feel like progress to you?",
        "I appreciate you sharing this with me. What would be a good next step for you?"
    ])

# Initialize session state for messages and conversation state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm here to provide mental health support. How are you feeling today?"}
    ]

# Enhanced conversation state tracking
if "conversation_state" not in st.session_state:
    st.session_state.conversation_state = {
        "tone": "neutral",             # Can be casual, neutral, or formal
        "previous_issues": [],         # Track previously discussed issues
        "session_length": 0,           # Track number of exchanges
        "client_name": None,           # Store client's name if shared
        "recurring_topics": {},        # Track frequency of topics
        "last_emotion": "neutral",     # Track last detected emotion
        "session_start": datetime.now().strftime("%Y-%m-%d %H:%M"),  # Track session time
        "crisis_detected": False,      # Flag if crisis was detected
        "rapport_level": "initial",    # Track therapeutic rapport (initial, building, established)
        "follow_up_topics": [],        # Topics to potentially follow up on
        "client_style": "neutral"      # Client communication style
    }

# Initialize session state for tracking previous responses to avoid repetition
if "previous_responses" not in st.session_state:
    st.session_state.previous_responses = {
        "greeting": [],
        "validation": [],
        "followup": [],
        "depression": [],
        "anxiety": [],
        "general": [],
        # Add other categories as needed
    }

# Function to get a unique response that hasn't been used recently
def get_unique_response(category, responses_list, max_history=5):
    """Select a response that hasn't been used in recent history with enhanced randomization"""
    # If we don't have this category in tracking, initialize it
    if category not in st.session_state.previous_responses:
        st.session_state.previous_responses[category] = []
    
    # Get the list of previously used responses for this category
    previous = st.session_state.previous_responses[category]
    
    # Filter out responses that have been used recently
    available_responses = [r for r in responses_list if r not in previous]
    
    # If we have very few responses available, add more diversity by slight modifications
    if len(available_responses) <= 1 and len(responses_list) > 1:
        # Create variants of existing responses
        variants = []
        for resp in responses_list:
            # Skip recently used responses
            if resp in previous[-2:]:  # Avoid the most recently used ones
                continue
                
            # Create variants with slight modifications
            if len(resp) > 20:  # Only for longer responses
                words = resp.split()
                if len(words) > 5:
                    # Replace some common words with synonyms
                    synonyms = {
                        "difficult": ["challenging", "tough", "hard", "demanding"],
                        "feel": ["experience", "sense", "perceive"],
                        "understand": ["get", "comprehend", "grasp", "see"],
                        "important": ["crucial", "vital", "essential", "key"],
                        "help": ["assist", "support", "aid"],
                        "talk": ["chat", "discuss", "share", "open up"],
                        "feeling": ["emotion", "sentiment", "state of mind"],
                        "good": ["great", "positive", "beneficial", "helpful"],
                        "think": ["believe", "consider", "feel", "reckon"],
                        "look": ["seem", "appear", "come across"],
                        "like": ["such as", "for example", "for instance", "similar to"]
                    }
                    
                    # Try to replace one word with a synonym
                    for i, word in enumerate(words):
                        word_lower = word.lower().strip('.,?!')
                        if word_lower in synonyms and random.random() < 0.7:  # 70% chance to replace
                            replacement = random.choice(synonyms[word_lower])
                            # Preserve capitalization
                            if word[0].isupper():
                                replacement = replacement.capitalize()
                            words[i] = replacement
                            break
                    
                    variant = ' '.join(words)
                    if variant != resp:
                        variants.append(variant)
        
        # Add variants to available responses
        available_responses.extend(variants)
    
    # If all responses have been used, just get a random one that's least recently used
    if not available_responses:
        # Prioritize responses used longest ago
        response = responses_list[random.randint(0, len(responses_list)-1)]
    else:
        # Select a random response from available options with weighted probability
        # (favor ones that weren't used recently but not in the previous list)
        weights = [1.0] * len(available_responses)
        for i, resp in enumerate(available_responses):
            if resp in st.session_state.previous_responses.get(category, []):
                # Reduce weight for recently used responses
                position = st.session_state.previous_responses[category].index(resp)
                recency_penalty = 0.5 ** (len(st.session_state.previous_responses[category]) - position)
                weights[i] *= recency_penalty
        
        # Normalize weights
        if sum(weights) > 0:
            weights = [w/sum(weights) for w in weights]
            response = random.choices(available_responses, weights=weights, k=1)[0]
        else:
            response = random.choice(available_responses)
    
    # Update the history, keeping only the most recent ones
    previous.append(response)
    if len(previous) > max_history:
        previous.pop(0)  # Remove the oldest response
    
    st.session_state.previous_responses[category] = previous
    return response

# Add a function to create HTML components for speech synthesis
def text_to_speech_button(text, auto_play=False, button_text="🔊"):
    """Create a button that speaks text when clicked."""
    # Clean text for speech (remove markdown, etc.)
    clean_text = text.replace('"', '\\"').replace('\n', ' ')
    
    # JavaScript code for speech synthesis
    js_code = f"""
    <div style="display:flex;justify-content:flex-end;margin-top:5px;">
        <button class="speech-button" onclick="speakText('{clean_text}')" title="Listen to this message">
            {button_text}
        </button>
    </div>
    
    <script>
        // Only define the function once
        if (typeof window.speakText !== 'function') {{
            window.isSpeaking = false;
            window.currentUtterance = null;
            
            window.speakText = function(text) {{
                // Check if speech synthesis is available
                if (!('speechSynthesis' in window)) {{
                    alert('Sorry, your browser does not support text-to-speech!');
                    return;
                }}
                
                // Stop any current speech
                if (window.isSpeaking) {{
                    window.speechSynthesis.cancel();
                }}
                
                // Create a new utterance
                const utterance = new SpeechSynthesisUtterance(text);
                window.currentUtterance = utterance;
                
                // Set properties
                utterance.rate = 1.0;
                utterance.pitch = 1.1;
                utterance.volume = 1.0;
                
                // Try to find a female voice
                window.speechSynthesis.onvoiceschanged = function() {{
                    const voices = window.speechSynthesis.getVoices();
                    const femaleVoice = voices.find(voice => 
                        voice.name.includes('Female') || 
                        voice.name.includes('female') || 
                        voice.name.includes('Samantha') ||
                        voice.name.includes('Lisa')
                    );
                    
                    if (femaleVoice) {{
                        utterance.voice = femaleVoice;
                    }}
                }};
                
                // Event when speech ends
                utterance.onend = function() {{
                    window.isSpeaking = false;
                    window.currentUtterance = null;
                }};
                
                // Speak
                window.isSpeaking = true;
                window.speechSynthesis.speak(utterance);
            }};
        }}
        
        {f"setTimeout(function() {{ speakText('{clean_text}'); }}, 3000);" if auto_play else ""}
    </script>
    """
    
    return st.components.v1.html(js_code, height=40)

# Analyze client's communication style with enhanced Gen Z detection
def detect_client_style(text):
    """Detect the client's communication style with more nuanced categories including Gen Z speech patterns"""
    text = text.lower()
    
    # Default style score counters
    casual_score = 0
    formal_score = 0
    gen_z_score = 0
    
    # Casual indicators
    casual_indicators = [
        "hey", "yo", "sup", "lol", "haha", "yeah", "yep", "nope", 
        "gonna", "wanna", "dunno", "gotta", "kinda", "sorta",
        "u ", "ur ", "r u", "y'all", "ain't", "idk", "tbh", "omg",
        "like", "literally", "basically", "actually", "totally",
        "thx", "btw", "bc", "cuz", "cause", 
        "cool", "awesome", "ok", "k", "lmao", "lmfao", "rofl",
        "whatever", "anyways", "anyway", "i mean", "i guess", 
        "so", "just", "really", "pretty much", "kinda"
    ]
    
    # Gen Z specific indicators
    gen_z_indicators = [
        # Common Gen Z text shorthand
        "ngl", "fr", "rn", "slay", "no cap", "cap", "based", "cringe", "sus", "vibes", "vibe check",
        "bestie", "bestie energy", "hit different", "bet", "oof", "yeet", "fam", "bruh", "bruv",
        "lit", "fire", "goat", "lowkey", "highkey", "tea", "spill the tea", "mood", "facts",
        "sending me", "living for", "dead", "i'm dead", "ded", "im ded", "sending",
        "rent free", "lives in my head", "understood the assignment",
        
        # Stylistic patterns
        "*", "_", "~", "💀", "😭", "🤌", "✨", "🔥", "👀", "👁️👄👁️", "💅",
        
        # Text formatting
        "!!!!", "???", "!?!?", "SCREAMING", "THIS", "THAT", "LITERALLY",
        "i-", "and i oop", "sksksk", "periodt", "period", "purr", "as you should",
        
        # Emphasis patterns
        "sooo", "uhhh", "umm", "hmm", "lmaooo", "bahaha", "hehe", "heehee",
        
        # Casual abbreviations
        "tysm", "ily", "istg", "omfg", "wtf", "wth", "af", "mf", "bs", "nbd", "fomo", "yolo",
        
        # Internet culture references
        "main character", "villain era", "red flag", "green flag", "toxic", "gaslighting", "gatekeeping",
        "aesthetic", "core", "maxxing", "pilled", "moment", "era", "arc"
    ]
    
    # Formal indicators (well-structured, proper grammar)
    formal_indicators = [
        "hello", "good morning", "good afternoon", "good evening", "greetings",
        "sincerely", "regards", "appreciate your", "thank you", "please",
        "would you", "could you", "might I", "I would like to", "I am", "we are",
        "however", "therefore", "furthermore", "in addition", "moreover",
        "consequently", "thus", "hence", "accordingly", "subsequently",
        "in my opinion", "I believe", "I think", "indeed", "certainly",
        "undoubtedly", "precisely", "specifically", "particularly",
        "in conclusion", "to summarize", "in summary", "to conclude"
    ]
    
    # Check for casual indicators
    casual_count = sum(1 for indicator in casual_indicators if indicator in text)
    
    # Check for Gen Z specific language
    gen_z_count = sum(1 for indicator in gen_z_indicators if indicator in text)
    
    # Check for formal language patterns
    formal_count = sum(1 for indicator in formal_indicators if indicator in text)
    
    # Check for multiple exclamation/question marks (casual)
    multiple_marks = re.search(r'[!?]{2,}', text)
    if multiple_marks:
        casual_score += 1
        gen_z_score += 0.5  # Gen Z tends to use more punctuation for emphasis
    
    # Check for CAPS LOCK usage (Gen Z emphasis)
    caps_words = re.findall(r'\b[A-Z]{3,}\b', text)
    if caps_words:
        gen_z_score += len(caps_words)
    
    # Check for emoji usage
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F700-\U0001F77F"  # alchemical symbols
        u"\U0001F780-\U0001F7FF"  # Geometric Shapes
        u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess Symbols
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U000024C2-\U0001F251" 
        "]+", flags=re.UNICODE)
    
    emojis = emoji_pattern.findall(text)
    if emojis:
        casual_score += 1
        gen_z_score += len(emojis)  # Gen Z tends to use more emojis
    
    # Check for message length (longer messages tend to be more formal)
    word_count = len(text.split())
    if word_count < 10:
        casual_score += 1
    elif word_count > 40:
        formal_score += 1
    
    # Check for punctuation and capitalization (formal writing often has better punctuation)
    sentences = re.split(r'[.!?]+', text)
    properly_capitalized = sum(1 for s in sentences if s.strip() and s.strip()[0].isupper())
    
    # If most sentences are properly capitalized, increase formal score
    if sentences and properly_capitalized / len(sentences) > 0.7:
        formal_score += 2
    else:
        casual_score += 1
        
    # Check for abbreviations without apostrophes (casual)
    if re.search(r'\b(dont|cant|wont|isnt|arent|didnt|wouldnt|couldnt|shouldnt|wasnt|werent)\b', text):
        casual_score += 1
    
    # Add base scores from keyword counts
    casual_score += casual_count
    gen_z_score += gen_z_count
    formal_score += formal_count
    
    # Final determination with three-way comparison
    if gen_z_score > casual_score and gen_z_score > formal_score:
        return "gen_z"
    elif casual_score > formal_score:
        return "casual"
    else:
        return "formal"

# Function to generate contextual reflective response
def generate_reflective_response(issue, prompt):
    # Extract potential emotions
    emotions = extract_emotions(prompt)
    emotion = emotions[0] if emotions else "concerned"
    
    # Create a reflective response that mirrors back the content
    templates = RESPONSES["reflective"]
    reflective = random.choice(templates).format(emotion=emotion, topic=issue)
    
    return reflective

# Update memory and track recurring topics
def update_conversation_memory(prompt, issue):
    # Extract potential name if not already known
    if not st.session_state.conversation_state["client_name"]:
        name = extract_names(prompt)
        if name:
            st.session_state.conversation_state["client_name"] = name
    
    # Track topic frequency
    if issue in st.session_state.conversation_state["recurring_topics"]:
        st.session_state.conversation_state["recurring_topics"][issue] += 1
    else:
        st.session_state.conversation_state["recurring_topics"][issue] = 1
    
    # Add to follow-up topics if mentioned more than once
    if st.session_state.conversation_state["recurring_topics"][issue] > 1:
        if issue not in st.session_state.conversation_state["follow_up_topics"]:
            st.session_state.conversation_state["follow_up_topics"].append(issue)
    
    # Update last emotion
    emotions = extract_emotions(prompt)
    if emotions:
        st.session_state.conversation_state["last_emotion"] = emotions[0]
    
    # Update rapport level based on session length
    if st.session_state.conversation_state["session_length"] > 5:
        st.session_state.conversation_state["rapport_level"] = "building"
    if st.session_state.conversation_state["session_length"] > 10:
        st.session_state.conversation_state["rapport_level"] = "established"

# Generate specific therapeutic suggestions based on issue
def generate_therapeutic_suggestions(issue):
    suggestions = {
        "anxiety": [
            "Practice the 4-7-8 breathing technique: breathe in for 4 seconds, hold for 7 seconds, exhale for 8 seconds.",
            "Try the STOP technique when feeling anxious: Stop, Take a breath, Observe your thoughts, Proceed mindfully.",
            "Consider downloading a meditation app like Calm or Headspace for guided anxiety relief exercises.",
            "Keep a worry journal to externalize anxious thoughts and examine them objectively."
        ],
        "depression": [
            "Set one small achievable goal each morning, even if it's just making your bed or taking a shower.",
            "Try to spend 10-15 minutes outside in natural sunlight each day, which can help regulate mood.",
            "Consider a gratitude practice - write down three things you appreciate each day, no matter how small.",
            "Reach out to one person in your support network, even with just a brief text message."
        ],
        "stress": [
            "Try body scanning meditation - focus attention slowly from head to toe, relaxing each muscle group.",
            "Practice time blocking your day to create periods of focus and scheduled breaks.",
            "Consider the 'two-minute rule' - if a task takes less than two minutes, do it immediately to reduce mental load.",
            "Create clear boundaries between work and personal time with a specific end-of-work ritual."
        ],
        "sleep": [
            "Try to maintain a consistent sleep schedule, even on weekends, to regulate your body's natural clock.",
            "Create a relaxing bedtime routine that signals to your body it's time for sleep.",
            "Avoid screens 1-2 hours before bed, or use blue light blocking glasses if screen use is necessary.",
            "Keep your bedroom cool (around 65°F/18°C) which is optimal for sleep for most people."
        ],
        "relationship": [
            "Practice active listening - focus on understanding rather than formulating your response.",
            "Try the XYZ formula for addressing concerns: 'When you do X in situation Y, I feel Z.'",
            "Schedule regular check-ins with important people in your life to maintain connection.",
            "Consider writing letters to express complex feelings if verbal communication is difficult."
        ],
        "work": [
            "Try the Pomodoro technique - work for 25 minutes, then take a 5-minute break to maintain focus.",
            "Create a priority matrix by categorizing tasks as urgent/important to focus your energy effectively.",
            "Consider setting up your workspace ergonomically to reduce physical strain during work.",
            "Practice saying 'no' to additional responsibilities when your plate is already full.",
            "Create clear boundaries between work and personal life, like turning off notifications after hours.",
            "Schedule short breaks throughout your workday to reset and reduce mental fatigue.",
            "Consider identifying what specific aspects of your job cause the most stress, which can help you develop targeted coping strategies.",
            "Try to build a support network of colleagues who understand your workplace challenges.",
            "If possible, speak with your manager about your workload or specific stressors that could be addressed.",
            "Practice self-compassion when work tasks don't go perfectly - remind yourself that everyone faces workplace challenges."
        ],
        "trauma": [
            "Try the 5-4-3-2-1 grounding technique when flashbacks occur: name 5 things you see, 4 things you touch, 3 things you hear, 2 things you smell, and 1 thing you taste.",
            "Consider keeping a journal to track triggers and develop awareness of your responses.",
            "Practice self-compassion by speaking to yourself as you would to a friend going through similar experiences.",
            "Explore trauma-informed yoga or gentle movement practices designed for trauma recovery."
        ],
        "family": [
            "Consider establishing clear boundaries with family members about what behaviors are acceptable.",
            "Try scheduled 'family meetings' to address concerns in a structured, calm environment.",
            "Practice the pause - taking a deep breath before responding to triggering family interactions.",
            "Consider writing out your thoughts before difficult family conversations to organize your thinking."
        ],
        "general": [
            "Consider starting a daily journaling practice to process your thoughts and feelings.",
            "Try incorporating a brief mindfulness practice into your daily routine.",
            "Establish a regular exercise routine, even if it's just a short daily walk.",
            "Consider creating a self-care plan with activities that nurture your physical, emotional, and mental well-being."
        ]
    }
    
    if issue in suggestions:
        return random.choice(suggestions[issue])
    return random.choice(suggestions["general"])

# Enhanced sympathetic responses
SYMPATHY_RESPONSES = {
    "anxiety": [
        "That sounds incredibly difficult to deal with. Anxiety can feel so overwhelming and all-consuming.",
        "I'm truly sorry you're experiencing such intense anxiety. It can be so exhausting to have your mind constantly racing.",
        "Living with anxiety is genuinely challenging. I hear how much this is affecting your daily life.",
        "It takes real courage to talk about anxiety. I really appreciate you sharing something so personal."
    ],
    "depression": [
        "I'm so sorry you're feeling this way. Depression can make even the smallest tasks feel insurmountable.",
        "That sounds incredibly difficult. Depression has a way of draining the color from everything.",
        "I truly hear how much you're struggling right now. Depression is such a heavy burden to carry.",
        "Thank you for sharing something so personal. It takes real strength to talk about these feelings."
    ],
    "stress": [
        "That level of stress sounds genuinely overwhelming. I'm sorry you're carrying such a heavy load right now.",
        "It's really hard when stress builds up like that. I can hear how much pressure you're under.",
        "Being under constant stress is so draining. I'm sorry you're going through this difficult time.",
        "I can hear how overwhelmed you're feeling. It's a lot to handle all at once."
    ],
    "sleep": [
        "Sleep problems can be truly debilitating. I'm sorry you're struggling with this essential need.",
        "Not getting proper rest affects everything else. I hear how difficult this is for you.",
        "Sleep difficulties can be so frustrating and exhausting. This must be really hard on you.",
        "I'm sorry you're dealing with such challenging sleep issues. That can wear you down on every level."
    ],
    "relationship": [
        "Relationship challenges can be deeply painful. I'm sorry you're going through this difficult situation.",
        "That sounds really hurtful. Relationship struggles can touch our core in such profound ways.",
        "I can hear how much this relationship situation is affecting you. These kinds of challenges can be so difficult.",
        "I'm truly sorry you're experiencing this pain. Relationship difficulties can feel so overwhelming."
    ],
    "work": [
        "Work stress can seep into every part of life. I'm sorry you're dealing with such a challenging situation.",
        "That sounds incredibly difficult to manage. Work issues can feel so consuming and unavoidable.",
        "I can hear how much this work situation is affecting you. It's hard when something so central to daily life becomes a source of distress.",
        "I'm sorry you're experiencing such difficulties at work. These kinds of challenges can be so draining.",
        "Job stress can be particularly overwhelming because we spend so much of our time at work. I understand how draining this must be for you.",
        "I hear that you're really stressed about your job. Work pressures can build up and affect our entire wellbeing.",
        "It sounds like your job is causing you significant stress right now. That's really tough to navigate day after day.",
        "Work stress is so challenging because it affects our financial security, identity, and daily routine all at once. I'm sorry you're going through this."
    ],
    "trauma": [
        "I'm deeply sorry you experienced that. Trauma leaves real wounds that deserve acknowledgment and care.",
        "Thank you for trusting me with something so personal. Trauma can affect us in profound ways.",
        "I want to acknowledge the pain of what you've been through. These experiences can have such deep impacts.",
        "I hear you, and I believe you. What you experienced matters, and so does your healing journey."
    ],
    "family": [
        "Family issues can be uniquely painful because they touch our earliest bonds. I'm truly sorry you're going through this.",
        "That sounds really difficult. Family relationships carry so much history and emotional weight.",
        "I can hear how much these family dynamics are affecting you. These patterns can be so challenging to navigate.",
        "I'm sorry you're experiencing these family difficulties. These relationships can be complicated in ways others may not fully understand."
    ],
    "general": [
        "That sounds really difficult. I'm genuinely sorry you're going through this.",
        "I appreciate you sharing something so personal. It takes courage to talk about these challenges.",
        "I can hear how much this is affecting you. It makes sense that you would feel this way.",
        "Thank you for trusting me with this. What you're experiencing matters, and your feelings are valid."
    ]
}

# Function to check for hopelessness indicators
def check_for_hopelessness(text):
    """Detect indicators of hopelessness that might not trigger full crisis response"""
    text = text.lower()
    
    # Hopelessness indicators - more comprehensive
    hopelessness_indicators = [
        "no point", "pointless", "hopeless", "never get better", 
        "always be this way", "nothing helps", "nothing works",
        "no future", "no hope", "won't improve", "can't improve",
        "tired of trying", "given up", "why bother", "what's the use",
        "nothing to live for", "no reason to", "can't see a way",
        "never ending", "endless", "forever", "permanent",
        "no way out", "trapped", "stuck forever", "no escape",
        "beyond help", "too far gone", "unfixable", "can't be fixed",
        "life is meaningless", "doesn't matter anymore", "no meaning"
    ]
    
    # Check each indicator
    for indicator in hopelessness_indicators:
        if indicator in text:
            return True
    
    # Additional check for phrases like "I'll never..." + negative outcome
    never_patterns = [
        r"i'?ll never be happy",
        r"i'?ll never get better",
        r"i'?ll never recover",
        r"i'?ll never find",
        r"i'?ll never be good enough",
        r"i'?ll never be loved",
        r"i'?ll never succeed",
        r"i'?ll never escape",
        r"i'?ll never be free"
    ]
    
    for pattern in never_patterns:
        if re.search(pattern, text):
            return True
    
    return False

# Function to extract potential client name
def extract_name(text):
    """Extract potential client name from the message for personalization"""
    # First, try to find explicit name mentions
    name_patterns = [
        r"my name is (\w+)",
        r"i'?m (\w+)",
        r"call me (\w+)",
        r"it'?s (\w+)"
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, text.lower())
        if match:
            name = match.group(1)
            # Only accept reasonable name lengths (2-15 chars) to avoid false positives
            if 2 <= len(name) <= 15 and name not in [
                "sorry", "just", "really", "actually", "honestly", "feeling", "trying",
                "going", "getting", "having", "being", "thinking", "wondering", "hoping",
                "here", "there", "everywhere", "nowhere", "somewhere", "inside", "outside",
                "depressed", "anxious", "stressed", "tired", "exhausted", "worried", "concerned"
            ]:
                return name.capitalize()
    
    return None

# Function to detect direct emotion statements
def detect_direct_emotion(text):
    text = text.lower().strip()
    
    # Expanded emotion list with synonyms
    emotions = {
        "sad": ["sad", "unhappy", "depressed", "down", "blue", "miserable", "heartbroken", "gloomy", 
                "disappointed", "upset", "disheartened", "grief", "sorrow", "tearful", "hurt", "broken",
                "despair", "devastated", "empty", "lost", "alone", "lonely", "abandoned", "crying"],
        "angry": ["angry", "mad", "furious", "annoyed", "irritated", "frustrated", "rage", "outraged", 
                 "pissed", "resentful", "hostile", "bitter", "enraged", "hate", "fury", "disgusted", 
                 "contempt", "dislike", "aversion", "fed up"],
        "anxious": ["anxious", "nervous", "worried", "scared", "afraid", "fearful", "terrified", "panicked", 
                   "uneasy", "tense", "apprehensive", "stressed", "restless", "jittery", "on edge", 
                   "overwhelmed", "freaked out", "dread", "panic", "fretful", "troubled", "concerned"],
        "neutral": ["okay", "fine", "alright", "neutral", "so-so", "meh", "indifferent", "neither", 
                   "average", "middle", "normal", "usual"],
        "confused": ["confused", "puzzled", "perplexed", "unsure", "uncertain", "don't understand", "lost", 
                    "disoriented", "bewildered", "unclear", "ambivalent", "mixed feelings"],
        "hopeful": ["hopeful", "optimistic", "encouraged", "confident", "looking forward", "positive", 
                   "promising", "hopeful", "expect", "anticipate", "believe", "trust"],
        "tired": ["tired", "exhausted", "weary", "fatigued", "drained", "spent", "sleepy", "worn out", 
                 "burned out", "lethargic"],
        "grateful": ["grateful", "thankful", "appreciative", "blessed", "fortunate", "appreciate"],
        "happy": ["happy", "glad", "joy", "excited", "great", "good", "wonderful", "fantastic", "amazing", 
                 "delighted", "pleased", "cheerful", "content", "thrilled", "ecstatic", "love", 
                 "smile", "laugh", "enjoy", "fun", "bright", "positive", "blessed"],
        "numb": ["numb", "empty", "hollow", "void", "nothing", "emotionless", "detached", "disconnected"],
        "worthless": ["worthless", "useless", "failure", "inadequate", "not enough", "undeserving"],
        "lonely": ["lonely", "alone", "isolated", "abandoned", "unwanted", "rejected", "unloved"],
        "sick": ["sick", "ill", "unwell", "nauseous", "dizzy", "pain", "ache", "hurt physically"],
        "grief": ["grief", "mourning", "loss", "bereavement", "missing someone", "lost someone"],
        "burnout": ["burnout", "unmotivated", "can't focus", "can't concentrate", "no energy", "no motivation"],
        "relationship_concern": ["relationship", "partner", "boyfriend", "girlfriend", "spouse", "dating", 
                               "marriage", "connection", "trust issues", "commitment", "cheating", "infidelity",
                               "ghosted", "breakup", "toxic relationship", "red flags", "abusive"],
        "heartbreak": ["heartbreak", "heartbroken", "heart broken", "broken heart", "miss him", "miss her", 
                     "miss them", "broke up", "breakup", "broke my heart", "love of my life", "left me", 
                     "broke up with me", "dumped me", "dumped", "end of relationship", "relationship ended"],
        "bad_day": ["bad day", "rough day", "tough day", "awful day", "terrible day", "worst day", 
                  "day sucked", "horrible day", "shitty day", "crappy day", "hard day"]
    }
    
    import re
    
    # First, check for common negation phrases in the entire text
    has_negation = any(neg in text for neg in ["not feeling", "don't feel", "isn't", "aren't", "don't", "doesn't", "didn't", 
                                              "can't", "cannot", "never", "no longer", "not good", "not well", "not happy", 
                                              "not fine", "not okay", "not ok", "not feeling good", "not feeling well", 
                                              "not feeling great", "not doing well", "not doing good"])
    
    # Handle direct statements with negation separately
    if has_negation:
        # For "not feeling good/well/great" specifically
        if any(phrase in text for phrase in ["not feeling good", "not feeling well", "not feeling great", 
                                            "not doing well", "not doing good", "don't feel good", "don't feel well",
                                            "not good", "not well", "not okay", "not ok"]):
            return "sad"  # Default to sad for negative wellness statements
        
        # For specific negated emotions
        if "not feeling happy" in text or "don't feel happy" in text:
            return "sad"
        if "not feeling sad" in text or "don't feel sad" in text:
            return "neutral"
        if "not feeling anxious" in text or "don't feel anxious" in text or "not anxious" in text:
            return "neutral"
        if "not angry" in text or "not feeling angry" in text or "don't feel angry" in text:
            return "neutral"
    
    # Check for bad day patterns
    bad_day_patterns = [
        r"(?:today|my day|the day) (?:sucked|was bad|was awful|was terrible|was horrible|was rough|was tough|was the worst)",
        r"(?:having|had|having such|had such) a (?:bad|rough|tough|terrible|awful|horrible|shit|crappy) day",
        r"(?:everything|nothing) (?:went|is going|has gone) (?:wrong|right)",
        r"(?:messed|screwed|fucked) everything up",
        r"everyone(?:'s| is| has been) (?:annoying|irritating|frustrating|bothering me)",
        r"(?:feel|feeling|want|wanting|going) to cry",
        r"(?:it's|its) (?:just|been) one of those days",
        r"(?:tired|exhausted|done|sick|fed up) (?:of|with) everything",
        r"people (?:don't|do not|won't|can't) (?:get|understand) me",
        r"(?:life|everything) (?:feels|seems|is) (?:so|too|very) hard",
        r"(?:i feel|feeling) invisible",
        r"(?:i'm not|i am not|not) enough",
        r"(?:i'm|i am) (?:just|so|really|totally) done",
        r"nobody (?:cares|gives a shit|gives a damn)",
        r"everything (?:is|keeps) piling up",
        r"(?:wanna|want to) disappear",
        r"(?:thoughts|mind) (?:won't stop|keeps|keep) racing",
        r"(?:too|so) exhausted",
        r"no one (?:notices|sees|appreciates) (?:my|me|the) efforts",
        r"(?:smiled|smiling|pretending) (?:but|while) (?:dying|dead|broken|hurting) inside",
        r"(?:want|wish) the day (?:to|would) end",
        r"(?:don't|do not) know how to feel better",
        r"(?:yelled|shouted|snapped|lashed out) at someone",
        r"stayed in bed all day",
        r"(?:feel|feeling) stuck",
        r"(?:ruined|destroyed|wrecked) everything",
        r"(?:people|everyone|they) expect (?:too|so) much",
        r"(?:wish|want) (?:i was|i were|to be) someone else",
        r"(?:just|only|really) want peace",
        r"nothing (?:feels|seems) worth it"
    ]
    
    for pattern in bad_day_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            # Determine the specific type of bad day experience
            if any(phrase in text.lower() for phrase in ["invisible", "not seen", "no one sees", "no one notices"]):
                return "feeling_invisible"
            elif any(phrase in text.lower() for phrase in ["piling up", "overwhelmed", "too much", "can't handle", "overwhelming"]):
                return "feeling_overwhelmed"
            elif any(phrase in text.lower() for phrase in ["messed up", "my fault", "blame myself", "ruined", "screwed up"]):
                return "self_criticism"
            elif any(phrase in text.lower() for phrase in ["don't understand", "don't get", "misunderstood"]):
                return "feeling_misunderstood"
            elif any(phrase in text.lower() for phrase in ["exhausted", "tired", "drained", "no energy", "worn out"]):
                return "emotional_exhaustion"
            else:
                return "bad_day"
    
    # Check for direct "I feel X" or "I am feeling X" or "I am X" statements
    direct_patterns = [
        r"i feel ([\w\s]+)",
        r"i am feeling ([\w\s]+)",
        r"i'm feeling ([\w\s]+)",
        r"feeling ([\w\s]+)",
        r"i am ([\w\s]+)",
        r"i'm ([\w\s]+)",
        r"i've been ([\w\s]+)",
        r"i've felt ([\w\s]+)",
        r"i just feel ([\w\s]+)",
        r"i don't feel ([\w\s]+)",
        r"i always feel ([\w\s]+)",
        r"i often feel ([\w\s]+)",
        r"i sometimes feel ([\w\s]+)"
    ]
    
    # Question patterns about emotions
    question_patterns = [
        r"why (?:do|am) i (?:feel|feeling) ([\w\s]+)",
        r"why (?:do|am) i (?:always|often|sometimes|constantly) ([\w\s]+)",
        r"why can't i (?:just be|feel|stop feeling) ([\w\s]+)",
        r"why (?:do|am) i so ([\w\s]+)",
        r"is it normal to feel ([\w\s]+)",
        r"is it okay to feel ([\w\s]+)",
        r"how do i stop feeling ([\w\s]+)",
        r"i don't know why i'm ([\w\s]+)",
        r"how do i ([\w\s]+)",
        r"why do i ([\w\s]+)",
        r"will this ([\w\s]+) ever ([\w\s]+)",
        r"what if ([\w\s]+)"
    ]
    
    # Indirect statements
    indirect_patterns = [
        r"i (?:just|don't|can't) want to (?:feel|be) ([\w\s]+)",
        r"i wish i wasn't ([\w\s]+)",
        r"i hate feeling ([\w\s]+)",
        r"i'm tired of being ([\w\s]+)",
        r"i can't take being ([\w\s]+)",
        r"i'm scared of ([\w\s]+)",
        r"i'm afraid of ([\w\s]+)",
        r"i can't stop thinking about ([\w\s]+)",
        r"people always ([\w\s]+)",
        r"nobody ([\w\s]+)",
        r"everyone ([\w\s]+)",
        r"i have no ([\w\s]+)",
        r"i'm jealous of ([\w\s]+)",
        r"i keep ([\w\s]+)"
    ]
    
    # Check direct patterns first
    for pattern in direct_patterns:
        match = re.search(pattern, text)
        if match:
            raw_emotion = match.group(1).strip()
            
            # Check for negation within the pattern
            if pattern.startswith(r"i don't") or "not" in raw_emotion:
                # If we're negating a positive emotion, return sad
                if any(pos in raw_emotion for pos in ["good", "great", "happy", "fine", "okay", "well"]):
                    return "sad"
                # If we're negating a negative emotion, return neutral
                if any(neg in raw_emotion for neg in ["sad", "angry", "anxious", "depressed", "bad"]):
                    return "neutral"
            
            # For "I am/feeling" with context
            words = raw_emotion.split()
            if "not" in words:
                try:
                    # Find the position of "not"
                    not_index = words.index("not")
                    # Check if there's a word after "not"
                    if not_index < len(words) - 1:
                        next_word = words[not_index + 1]
                        # Check if the next word is a positive emotion
                        if next_word in emotions["happy"] or next_word in ["good", "well", "great", "okay", "ok", "fine"]:
                            return "sad"
                except:
                    pass
            
            # Check against emotion synonyms
            for emotion, synonyms in emotions.items():
                if any(syn in raw_emotion for syn in synonyms):
                    return emotion
    
    # Then check question patterns
    for pattern in question_patterns:
        match = re.search(pattern, text)
        if match:
            raw_emotion = match.group(1).strip()
            for emotion, synonyms in emotions.items():
                if any(syn in raw_emotion for syn in synonyms):
                    return emotion
    
    # Finally check indirect patterns
    for pattern in indirect_patterns:
        match = re.search(pattern, text)
        if match:
            raw_emotion = match.group(1).strip()
            for emotion, synonyms in emotions.items():
                if any(syn in raw_emotion for syn in synonyms):
                    return emotion
    
    # Special cases for feeling "not good"
    if any(phrase in text for phrase in ["not good", "not well", "not ok", "not okay"]):
        return "sad"
    
    # Handle simple statements like "I am not feeling good" that might not match the patterns
    if "not feeling good" in text or "not feeling well" in text:
        return "sad"
    
    if "feeling good" in text or "feeling well" in text or "feeling better" in text:
        # Check for negation near the phrase
        if any(neg + " feeling" in text for neg in ["not", "don't", "doesn't", "didn't"]):
            return "sad"
        return "happy"
    
    # Specific relationship detection patterns
    relationship_patterns = [
        r"(?:always fall for|fall for) the wrong people",
        r"(?:my friends don't care|friends don't care|no one cares)",
        r"(?:scared|afraid) of being vulnerable",
        r"(?:people|others|they) (?:always|often) take advantage",
        r"(?:how do i|can i|help me) (?:fix|repair|heal|mend) (?:a|my|the) (?:relationship|marriage|connection)",
        r"(?:what if|afraid|scared) (?:they|he|she|people) leave",
        r"(?:no one|nobody) loves me",
        r"(?:why do i|i always|i keep) push people away",
        r"(?:can you|how do i|help me) trust again",
        r"(?:toxic|unhealthy) (?:friendships|relationships|people)",
        r"(?:what's|what is) a healthy relationship",
        r"(?:jealous|envious|insecure) (?:of|about) (?:my|their) (?:partner|friend|boyfriend|girlfriend)",
        r"(?:ghosted|ignored|abandoned|left) me",
        r"(?:attached|clingy|dependent) (?:quickly|easily|too|so)",
        r"(?:deal with|cope with|handle|get over) (?:a|the) breakup"
    ]
    
    for pattern in relationship_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return "relationship_concern"
    
    # Grief and loss patterns
    grief_patterns = [
        r"(?:lost|lose|losing|died|passed away|death) (?:someone|somebody|a person|him|her|them|family|friend)",
        r"(?:this pain|grief|mourning|sadness) (?:ever|never) (?:go away|end|stop|get better)",
        r"(?:can't stop|always|keep) thinking about (?:them|him|her|person|someone I lost)",
        r"(?:guilty|shame|bad) (?:for|about) moving on",
        r"(?:deal with|cope with|handle) (?:anniversary|birthday|holiday) (?:death|loss|since)",
        r"(?:expect|want|need) me to be okay",
        r"(?:didn't|couldn't|never) (?:get to|had a chance to) say goodbye",
        r"(?:part of me|piece of me|feel like) (?:is|has) gone",
        r"(?:support|help|be there for) someone who(?:'s| is) grieving",
        r"(?:miss|missing|think about) them every day"
    ]
    
    for pattern in grief_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return "grief"
    
    # Motivation and burnout patterns
    motivation_patterns = [
        r"(?:no|lost|lacking|don't have|zero) motivation",
        r"(?:get|getting|climb|leave|force myself) out of bed",
        r"(?:burned out|burnt out|burnout)",
        r"(?:can't|unable to|struggle to|don't) focus",
        r"(?:feel like|want to|thinking about) giving up",
        r"(?:tired of|exhausted from|sick of) pretending",
        r"(?:alone|lonely) in a crowd",
        r"(?:nobody|no one|none) notices me",
        r"(?:can't find|don't have|lost) (?:energy|will|desire) to care",
        r"(?:life has no|can't find|don't see|what's the) meaning"
    ]
    
    for pattern in motivation_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return "burnout"
    
    # Special cases
    if any(phrase in text for phrase in ["don't know who i am", "lost myself", "identity", "who am i"]):
        return "confused"
        
    if any(phrase in text for phrase in ["crying", "want to cry", "tears", "sobbing", "weeping"]):
        return "sad"
        
    if any(phrase in text for phrase in ["panic attack", "heart racing", "can't breathe", "hyperventilating"]):
        return "anxious"
        
    if any(phrase in text for phrase in ["hate myself", "self-hatred", "self-loathing"]):
        return "worthless"
    
    # Crisis patterns - trigger immediate support
    crisis_patterns = [
        r"(?:want to|thinking about|considering) (?:disappear|end it|die|death|suicide|kill myself)",
        r"(?:hurting|harm|hurt) myself",
        r"(?:would anyone|will anyone|does anyone|no one would) (?:care|miss|notice) if i was gone",
        r"(?:keep going|continue|live|survive) when it's (?:too much|overwhelming|unbearable)"
    ]
    
    for pattern in crisis_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return "crisis"
    
    return None

# Generate a response based on the input text and conversation history
def get_response(prompt):
    # Update conversation state
    st.session_state.conversation_state["session_length"] += 1
    
    # First check for crisis keywords for immediate support
    is_crisis, crisis_type = check_for_crisis_keywords(prompt)
    if is_crisis:
        # Update crisis detection flag
        st.session_state.conversation_state["crisis_detected"] = True
        
        if crisis_type == "self_harm":
            # Prepare suicide/self-harm crisis response
            # First a compassionate validation
            crisis_validation = get_unique_response("crisis_support", RESPONSES["crisis_support"])
            
            # Add an affirmation
            affirmation = get_unique_response("affirmations", RESPONSES["affirmations"])
            
            # Explicit crisis resources
            crisis_resources = """
            **Crisis Resources:**
            - National Suicide Prevention Lifeline: 988 or 1-800-273-8255
            - Crisis Text Line: Text HOME to 741741
            
            These services are available 24/7 and provide confidential support from trained counselors.
            """
            
            # Combine all parts
            return f"{crisis_validation}\n\n{affirmation}\n\n{crisis_resources}"
    
    # Check for direct emotion statements or special categories
    direct_emotion = detect_direct_emotion(prompt)
    
    if direct_emotion:
        # Handle direct emotion expressions with specific responses
        
        # Special case for "I love you" and similar
        if direct_emotion == "love_you":
            return "I appreciate your kind words. I'm here as a supportive space for you to explore your feelings and thoughts. How are you feeling today?"
            
        # Handle specialized heartbreak categories
        elif direct_emotion in ["heartbreak", "breakup_ghosting", "breakup_betrayal", "breakup_still_love", "breakup_comparison", "breakup_moving_on"]:
            response_parts = []
            
            # Add appropriate heartbreak response based on the specific type
            response_parts.append(get_unique_response(direct_emotion, RESPONSES[direct_emotion]))
            
            # Add a validation from the deep validation set
            response_parts.append(get_unique_response("validation_deep", RESPONSES["validation_deep"]))
            
            # Add a gentle question to continue the conversation
            if direct_emotion == "breakup_ghosting":
                response_parts.append("What would closure look like for you right now, even if it has to come from within?")
            elif direct_emotion == "breakup_betrayal":
                response_parts.append("How have you been caring for yourself through this betrayal?")
            elif direct_emotion == "breakup_still_love":
                response_parts.append("What parts of them or the relationship do you find yourself missing most?")
            elif direct_emotion == "breakup_comparison":
                response_parts.append("What would your healing journey look like if you weren't comparing it to theirs?")
            elif direct_emotion == "breakup_moving_on":
                response_parts.append("What small step toward your own happiness feels possible today?")
            else:
                response_parts.append("What aspect of this heartbreak has been most difficult for you to process?")
            
            return "\n\n".join(response_parts)
            
        elif direct_emotion == "grief":
            # For grief and loss
            response_parts = []
            response_parts.append(get_unique_response("grief_loss", RESPONSES["grief_loss"]))
            response_parts.append(get_unique_response("grief_coping", RESPONSES["grief_coping"]))
            response_parts.append(get_unique_response("validation_deep", RESPONSES["validation_deep"]))
            return "\n\n".join(response_parts)
            
        elif direct_emotion == "burnout":
            # For motivation and burnout
            response_parts = []
            response_parts.append(get_unique_response("motivation_burnout", RESPONSES["motivation_burnout"]))
            
            # Add specific suggestions based on the type of motivation issue
            if any(phrase in prompt.lower() for phrase in ["meaning", "purpose", "point", "worthwhile"]):
                response_parts.append(get_unique_response("meaning_purpose", RESPONSES["meaning_purpose"]))
            else:
                # General validation
                response_parts.append(get_unique_response("validation", RESPONSES["validation"]))
                
            # Add a gentle encouragement
            response_parts.append("Remember, it's okay to take small steps. Even tiny movements forward count.")
            
            return "\n\n".join(response_parts)
            
        elif direct_emotion == "crisis":
            # Handle crisis explicitly
            crisis_validation = get_unique_response("crisis_support", RESPONSES["crisis_support"])
            affirmation = get_unique_response("affirmations", RESPONSES["affirmations"])
            
            crisis_resources = """
            **Crisis Resources:**
            - National Suicide Prevention Lifeline: 988 or 1-800-273-8255
            - Crisis Text Line: Text HOME to 741741
            
            These services are available 24/7 and provide confidential support from trained counselors.
            """
            
            return f"{crisis_validation}\n\n{affirmation}\n\n{crisis_resources}"
        
        # Handle regular emotion expressions
        # Get response template for direct emotion
        templates = RESPONSES["direct_emotion"]
        response = get_unique_response("direct_emotion", templates).format(emotion=direct_emotion)
        
        # Add appropriate follow-up based on the emotion
        if direct_emotion in ["sad", "angry", "anxious", "depressed", "low", "down", "upset", 
                             "hurt", "lost", "overwhelmed", "stressed", "tired", "exhausted", 
                             "sick", "ill", "unwell", "worthless", "numb", "lonely"]:
            # Negative emotions get validation and coping strategies
            response += "\n\n" + get_unique_response("validation", RESPONSES["validation"])
            
            # Add a coping suggestion based on the emotion
            if direct_emotion in ["sad", "depressed", "low", "down"]:
                response += "\n\nSometimes when we're feeling low, small self-care activities can help. Could you try something gentle that usually brings you comfort, like listening to music or going for a short walk?"
            elif direct_emotion in ["angry", "upset"]:
                response += "\n\nWhen feeling angry, it can help to find healthy ways to express it. Taking deep breaths or doing something physical like a brisk walk might help release some of that tension."
            elif direct_emotion in ["anxious", "overwhelmed", "stressed"]:
                response += "\n\nGrounding techniques can be helpful when feeling anxious. Try the 5-4-3-2-1 technique: notice 5 things you can see, 4 things you can touch, 3 things you can hear, 2 things you can smell, and 1 thing you can taste."
            elif direct_emotion in ["tired", "exhausted"]:
                response += "\n\nIt sounds like you might need some rest. Sometimes our bodies and minds signal when we need to slow down. Is there a way you could take a break or do something restorative today?"
            elif direct_emotion in ["sick", "ill", "unwell"]:
                response += "\n\nI'm sorry you're not feeling well physically. Taking care of your body is an important part of mental health too. Make sure you're getting enough rest, fluids, and consider reaching out to a healthcare provider if needed."
            elif direct_emotion in ["worthless", "useless"]:
                response += "\n\nThat inner critic can be incredibly harsh. Remember that your worth isn't determined by your productivity or achievements. You have inherent value just by being you."
            elif direct_emotion in ["numb", "empty"]:
                response += "\n\nFeeling numb can be your mind's way of protecting you from overwhelming emotions. Sometimes gentle engagement with simple activities like taking a shower, going for a walk, or listening to music can help you reconnect."
            elif direct_emotion in ["lonely", "alone"]:
                response += "\n\nLoneliness can feel so heavy. Is there someone you could reach out to, even with a simple text? Sometimes even small connections can help ease that isolated feeling."
            elif direct_emotion in ["confused", "lost"]:
                response += "\n\nIt's okay to feel uncertain sometimes. Taking things one step at a time and focusing just on what's in front of you can help when things feel overwhelming or unclear."
        else:
            # Positive emotions get affirmation
            response += "\n\nIt's wonderful that you're feeling this way. What do you think has contributed to this positive feeling?"
        
        return response
    
    # Detect client communication style first to adjust response style
    client_style = detect_client_style(prompt)
    st.session_state.conversation_state["client_style"] = client_style
    
    # Detect if message contains hopelessness indicators
    is_hopeless = check_for_hopelessness(prompt)
    
    # Check if message contains any names for personalization (after 2 exchanges to avoid confusion)
    if st.session_state.conversation_state["session_length"] > 2 and not st.session_state.conversation_state["client_name"]:
        detected_name = extract_name(prompt)
        if detected_name:
            st.session_state.conversation_state["client_name"] = detected_name
            st.session_state.conversation_state["rapport_level"] = "building"
    
    # Extract emotions to track emotional state
    current_emotions = extract_emotions(prompt)
    primary_emotion = current_emotions[0] if current_emotions else "neutral"
    
    # Check if it's a conversational message
    conversation_type = detect_conversation_type(prompt)
    
    # Select response style based on client style
    response_style = client_style  # Use client style as default
    
    # Provide hopelessness support if detected
    if is_hopeless:
        response_parts = []
        
        # Add supportive message for hopelessness
        response_parts.append(get_unique_response("hopelessness_support", RESPONSES["hopelessness_support"]))
        
        # Add affirmation
        if random.random() < 0.5:
            response_parts.append(get_unique_response("affirmations_extended", RESPONSES["affirmations_extended"]))
        else:
            response_parts.append(get_unique_response("affirmations", RESPONSES["affirmations"]))
        
        # Add appropriate follow-up question to invite elaboration
        response_parts.append("If you'd like to share more about what you're experiencing, I'm here to listen.")
        
        # For Gen Z clients, make the language more relatable
        if client_style == "gen_z":
            # Replace formal phrases with more Gen Z friendly ones
            gen_z_response = "\n\n".join(response_parts)
            gen_z_response = gen_z_response.replace("I understand", "I get it")
            gen_z_response = gen_z_response.replace("difficult time", "rough time")
            gen_z_response = gen_z_response.replace("I'm here to listen", "I'm here for you")
            return gen_z_response
        
        return "\n\n".join(response_parts)
    
    # Handle new conversation types directly
    if conversation_type in ["personal_experience", "childhood_trauma", "relationship_loss", 
                            "identity_struggle", "life_transition", "seeking_understanding", 
                            "detailed_reflection", "deep_feelings"]:
        response_parts = []
        
        # Add appropriate response based on conversation type
        if conversation_type == "personal_experience":
            response_parts.append(get_unique_response("personal_experience", RESPONSES["personal_experience"]))
        elif conversation_type == "seeking_understanding":
            response_parts.append("Yes, I understand what you're sharing. Your experiences and feelings are valid.")
        elif conversation_type == "detailed_reflection":
            response_parts.append("That's a thoughtful reflection. It shows real self-awareness to notice these patterns.")
        elif conversation_type == "deep_feelings":
            response_parts.append(get_unique_response("validation_deep", RESPONSES["validation_deep"]))
        
        # Add an empathetic follow-up to deepen the conversation
        if client_style == "gen_z":
            followup_key = "followup_gen_z"  # Use Gen Z specific followups if available
        elif client_style == "casual":
            followup_key = "followup_casual"
        else:
            followup_key = "followup"
            
        # Fallback to casual if gen_z specific not available
        if followup_key == "followup_gen_z" and "followup_gen_z" not in RESPONSES:
            followup_key = "followup_casual"
            
        response_parts.append(get_unique_response(followup_key, RESPONSES[followup_key]))
        
        # For Gen Z clients, adjust language style
        if client_style == "gen_z":
            gen_z_response = "\n\n".join(response_parts)
            gen_z_response = gen_z_response.replace("I understand", "I get that")
            gen_z_response = gen_z_response.replace("appreciate", "love") 
            gen_z_response = gen_z_response.replace("helpful", "awesome")
            return gen_z_response
        
        return "\n\n".join(response_parts)
    
    # Handle specific conversation types directly
    if conversation_type in ["greeting", "how_are_you", "feeling_question", "gratitude", "about_bot", 
                            "help_request", "agreement", "disagreement", "question", "mood_statement",
                            "problem_statement"]:
        # Handle greetings with personalization if name is known
        if conversation_type == "greeting":
            if st.session_state.conversation_state["client_name"] and st.session_state.conversation_state["session_length"] > 2:
                # Personalized greeting with name
                response = get_unique_response("greeting_with_name", RESPONSES["greeting_with_name"]).format(name=st.session_state.conversation_state["client_name"])
            elif client_style == "gen_z":
                # If Gen Z specific greetings exist
                if "greeting_gen_z" in RESPONSES:
                    response = get_unique_response("greeting_gen_z", RESPONSES["greeting_gen_z"])
                else:
                    response = get_unique_response("greeting_casual", RESPONSES["greeting_casual"])
            elif client_style == "casual":
                response = get_unique_response("greeting_casual", RESPONSES["greeting_casual"])
            else:
                response = get_unique_response("greeting", RESPONSES["greeting"])
        else:
            # Try to use style-specific responses if available
            style_specific_key = f"{conversation_type}_{client_style}"
            if style_specific_key in RESPONSES:
                response = get_unique_response(style_specific_key, RESPONSES[style_specific_key])
            else:
                # Otherwise use standard response
                response = get_unique_response(conversation_type, RESPONSES[conversation_type])
            
        # If we have established some rapport and it's a casual conversation, add a follow-up
        if st.session_state.conversation_state["session_length"] > 2 and conversation_type in ["greeting", "how_are_you", "feeling_question"]:
            if client_style == "gen_z" and "followup_gen_z" in RESPONSES:
                followup_key = "followup_gen_z"
            elif client_style == "casual":
                followup_key = "followup_casual"
            else:
                followup_key = "followup"
                
            response = f"{response}\n\n{get_unique_response(followup_key, RESPONSES[followup_key])}"
            
        return response
    
    # For other types of messages, detect the issue
    issue = detect_issue(prompt)
    
    # Update conversation memory
    update_conversation_memory(prompt, issue)
    
    # Add the issue to previous issues list
    st.session_state.conversation_state["previous_issues"].append(issue)
    
    # Detect message length to adapt response length appropriately
    is_long_message = len(prompt.split()) > 30
    is_problem_sharing = len(prompt.split()) > 40 or primary_emotion in ["sad", "angry", "anxious", "confused"]
    
    # Choose response approach based on context
    response_parts = []
    
    # Handle new issue types with specific responses
    if issue in ["childhood_trauma", "relationship_loss", "identity_struggle", "life_transition"]:
        # Add specialized response for deep personal issues
        response_parts.append(get_unique_response(issue, RESPONSES[issue]))
        
        # Add deeper validation
        response_parts.append(get_unique_response("validation_deep", RESPONSES["validation_deep"]))
        
        # Add a therapeutic suggestion specific to the issue
        therapeutic_suggestion = generate_therapeutic_suggestions(issue)
        response_parts.append(f"When you're ready, {therapeutic_suggestion}")
        
        # Add extended affirmation
        response_parts.append(get_unique_response("affirmations_extended", RESPONSES["affirmations_extended"]))
        
        # For Gen Z clients, adjust language style
        if client_style == "gen_z":
            gen_z_response = "\n\n".join(response_parts)
            gen_z_response = gen_z_response.replace("I understand", "I get that")
            gen_z_response = gen_z_response.replace("appreciate", "love") 
            gen_z_response = gen_z_response.replace("helpful", "awesome")
            gen_z_response = gen_z_response.replace("When you're ready", "Whenever you feel ready")
            return gen_z_response
        
        return "\n\n".join(response_parts)
    
    # 1. Add sympathy response for problem sharing
    if is_problem_sharing:
        sympathy_responses = SYMPATHY_RESPONSES.get(issue, SYMPATHY_RESPONSES["general"])
        response_parts.append(get_unique_response(f"sympathy_{issue}", sympathy_responses))
    # Otherwise add validation for emotional content
    elif primary_emotion in ["sad", "angry", "anxious", "confused", "tired"] or st.session_state.conversation_state["rapport_level"] in ["building", "established"]:
        # Add validation for negative emotions
        response_parts.append(get_unique_response("validation", RESPONSES["validation"]))
    
    # 2. For longer client messages, add reflective response to show understanding
    if is_long_message:
        reflective = generate_reflective_response(issue, prompt)
        response_parts.append(reflective)
    else:
        # For shorter messages, provide the standard issue response
        # Try to use client style specific response if available
        style_specific_key = f"{issue}_{client_style}"
        if style_specific_key in RESPONSES:
            response_parts.append(get_unique_response(style_specific_key, RESPONSES[style_specific_key]))
        else:
            response_parts.append(get_unique_response(issue, RESPONSES[issue]))
    
    # 3. For problem sharing, add specific therapeutic suggestions/cures
    if is_problem_sharing:
        # Add more comprehensive solutions 70% of the time for ChatGPT-like responses
        if random.random() < 0.7 and "general_solutions" in RESPONSES:
            therapeutic_suggestion = get_unique_response("general_solutions", RESPONSES["general_solutions"])
            response_parts.append(therapeutic_suggestion)
        else:
            # Fall back to the specific issue suggestions
            therapeutic_suggestion = generate_therapeutic_suggestions(issue)
            if client_style == "gen_z":
                response_parts.append(f"Here's something that might help you out: {therapeutic_suggestion}")
            else:
                response_parts.append(f"Here's something that might help: {therapeutic_suggestion}")
        
        # 3a. Add an affirmation for more serious issues
        if issue in ["depression", "anxiety", "trauma"] or primary_emotion in ["sad", "angry", "anxious"]:
            # Use extended affirmations 20% of the time for variety
            if random.random() < 0.2:
                response_parts.append(get_unique_response("affirmations_extended", RESPONSES["affirmations_extended"]))
            else:
                response_parts.append(get_unique_response("affirmations", RESPONSES["affirmations"]))
    
    # 4. Choose follow-up approach based on context
    # If client seems distressed, focus on current issue rather than changing topics
    if primary_emotion in ["sad", "angry", "anxious"] and len(prompt) > 30:
        if client_style == "gen_z" and "followup_gen_z" in RESPONSES:
            followup_key = "followup_gen_z"
        elif client_style == "casual":
            followup_key = "followup_casual"
        else:
            followup_key = "followup"
        followup = get_unique_response(followup_key, RESPONSES[followup_key])
    elif st.session_state.conversation_state["follow_up_topics"] and st.session_state.conversation_state["session_length"] > 3:
        # After establishing some rapport, occasionally return to previously mentioned topics
        if random.random() < 0.3:
            # Follow up on a previous topic
            topic = random.choice(st.session_state.conversation_state["follow_up_topics"])
            followup = get_unique_response("continue_topic", RESPONSES["continue_topic"]).format(topic=topic)
        else:
            # Otherwise use appropriate follow-up style
            if client_style == "gen_z" and "followup_gen_z" in RESPONSES:
                followup_key = "followup_gen_z"
            elif client_style == "casual":
                followup_key = "followup_casual"
            else:
                followup_key = "followup"
            followup = get_unique_response(followup_key, RESPONSES[followup_key])
    else:
        # Default follow-up approach
        if client_style == "gen_z" and "followup_gen_z" in RESPONSES:
            followup_key = "followup_gen_z"
        elif client_style == "casual":
            followup_key = "followup_casual"
        else:
            followup_key = "followup"
        followup = get_unique_response(followup_key, RESPONSES[followup_key])
    
    response_parts.append(followup)
    
    # Combine parts with appropriate spacing
    response = "\n\n".join(response_parts)
    
    # If client's name is known, occasionally use it for personalization
    if st.session_state.conversation_state["client_name"] and random.random() < 0.4:
        # Try different positions to add the name for more natural feel
        if random.random() < 0.5 and "you" in response:
            response = response.replace("you", f"you, {st.session_state.conversation_state['client_name']}", 1)
        else:
            # Add name to beginning of one of the paragraphs
            parts = response.split("\n\n")
            if len(parts) > 1:
                index = random.randint(0, len(parts)-1)
                parts[index] = f"{st.session_state.conversation_state['client_name']}, {parts[index][0].lower() + parts[index][1:]}" if parts[index][0].isupper() else parts[index]
                response = "\n\n".join(parts)
    
    # Match client's communication style more closely
    if client_style in ["casual", "gen_z"] and st.session_state.conversation_state["rapport_level"] != "initial":
        # Make response more casual for casual clients after initial rapport
        response = response.replace("Would you like to", "Want to")
        response = response.replace("It is", "It's")
        response = response.replace("I am", "I'm")
        response = response.replace("you are", "you're")
        
        # Additional Gen Z style adjustments
        if client_style == "gen_z":
            response = response.replace("That is wonderful", "That's awesome")
            response = response.replace("That is great", "That's amazing")
            response = response.replace("That is good", "That's cool")
            response = response.replace("I understand", "I get it")
            response = response.replace("perhaps", "maybe")
            response = response.replace("feeling badly", "feeling down")
            
            # Add occasional emphasis for Gen Z if the message isn't crisis-related
            if not is_crisis and not is_hopeless and "crisis" not in prompt.lower():
                parts = response.split("\n\n")
                if parts and random.random() < 0.3:
                    # Add emphasis to a random short sentence
                    sentences = parts[0].split('. ')
                    if len(sentences) > 1:
                        short_sentences = [s for s in sentences if 10 <= len(s) <= 30]
                        if short_sentences:
                            idx = sentences.index(random.choice(short_sentences))
                            if random.random() < 0.5:
                                # All caps emphasis
                                sentences[idx] = sentences[idx].upper()
                            else:
                                # Add emphasis markers
                                sentences[idx] = f"*{sentences[idx]}*"
                            parts[0] = '. '.join(sentences)
                            response = '\n\n'.join(parts)
    
    return response

# Analyze anger level in violent thoughts
def analyze_anger_level(text):
    """Analyze the severity and intent of violent thoughts expressions"""
    text = text.lower()
    
    # Patterns indicating critical/immediate concern
    critical_patterns = [
        "going to", "gonna", "will", "planning to", "intend to", "about to",
        "decided to", "ready to", "prepared to", "want to kill", "want to hurt",
        "tonight", "tomorrow", "soon", "already have", "bought a", "have a gun",
        "have a knife", "weapon", "hunting them", "stalking", "following them",
        "deserve to die", "better off dead", "won't be missed", "do it soon",
        "can't stop myself", "losing control", "can't help it", "no choice",
        "they'll pay", "make them pay", "show them", "teach them a lesson",
        "end this", "solution", "only way", "final answer"
    ]
    
    # Venting patterns - anger without specific plan
    venting_patterns = [
        "so angry", "so mad", "furious", "pissed off", "hate them", 
        "can't stand", "drives me crazy", "makes me so mad", "sick of",
        "had enough", "fed up", "hate it when", "pisses me off",
        "tired of", "wish they would", "annoys me", "getting on my nerves",
        "rage", "raging", "fuming", "irritated", "bothers me", "bothering me"
    ]
    
    # Count matches for each category
    critical_count = sum(1 for pattern in critical_patterns if pattern in text)
    venting_count = sum(1 for pattern in venting_patterns if pattern in text)
    
    # Check for specific phrases that should elevate concern regardless of count
    immediate_concern_phrases = [
        "going to kill", "gonna kill", "will kill", "planning to kill", 
        "intend to hurt", "about to hurt", "tonight i will", "tomorrow i will",
        "loaded gun", "sharpened knife", "weapon ready", "they won't see it coming"
    ]
    
    for phrase in immediate_concern_phrases:
        if phrase in text:
            return "critical"
    
    # Determine anger level based on counts and specific phrases
    if critical_count >= 2 or (critical_count >= 1 and len(text.split()) < 20):
        return "critical"
    elif venting_count >= 3 or (venting_count >= 2 and "hate" in text):
        return "venting"
    else:
        return "processing"

# Function to detect and store topics for personalized conversations
def detect_and_store_topics(text):
    """Extract and store topics the client mentions for more personalized follow-ups"""
    # Initialize topics storage if not present
    if "mentioned_topics" not in st.session_state.conversation_state:
        st.session_state.conversation_state["mentioned_topics"] = {}
    
    # Topics to track
    topic_keywords = {
        "work": ["job", "career", "workplace", "boss", "coworker", "office", "work"],
        "school": ["school", "college", "university", "class", "professor", "teacher", "homework", "exam", "test", "study"],
        "family": ["family", "parent", "mother", "father", "mom", "dad", "sister", "brother", "sibling", "relative"],
        "relationship": ["girlfriend", "boyfriend", "partner", "spouse", "wife", "husband", "dating", "relationship"],
        "friend": ["friend", "friendship", "bestie", "bff", "acquaintance", "social life"],
        "health": ["health", "doctor", "illness", "symptom", "diagnosis", "medical", "hospital", "clinic"],
        "hobby": ["hobby", "music", "art", "reading", "game", "gaming", "sport", "exercise", "painting", "drawing", "writing"],
        "pet": ["pet", "dog", "cat", "bird", "animal", "puppy", "kitten"],
        "home": ["home", "house", "apartment", "roommate", "neighbor", "living situation", "rent", "mortgage"],
        "finance": ["money", "finance", "debt", "saving", "budget", "loan", "financial", "expense", "bill", "income"],
        "future": ["future", "goal", "plan", "dream", "aspiration", "ambition", "purpose", "direction"]
    }
    
    text_lower = text.lower()
    
    # Check for each topic
    for topic, keywords in topic_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                # Initialize or increment topic mention counter
                if topic in st.session_state.conversation_state["mentioned_topics"]:
                    st.session_state.conversation_state["mentioned_topics"][topic] += 1
                else:
                    st.session_state.conversation_state["mentioned_topics"][topic] = 1
                
                # Only track one mention per topic per message
                break
    
    # Add frequently mentioned topics to follow-up topics list
    frequently_mentioned = [topic for topic, count in st.session_state.conversation_state["mentioned_topics"].items() 
                           if count >= 2 and topic not in st.session_state.conversation_state["follow_up_topics"]]
    
    for topic in frequently_mentioned:
        if topic not in st.session_state.conversation_state["follow_up_topics"]:
            st.session_state.conversation_state["follow_up_topics"].append(topic)

# Streamlit UI
if __name__ == "__main__":
    st.set_page_config(
        page_title="Sunshine - Mental Wellness Companion",
        page_icon="☀️",
        layout="wide",
        initial_sidebar_state="collapsed"  # Start with sidebar collapsed on mobile
    )

    # Custom CSS for a more uplifting appearance with responsive design
    st.markdown("""
    <style>
        /* Overall color scheme and fonts - Gen Z Aesthetic */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
        
        .main {
            background-color: #0f0f1a;
            color: #e0e0ff;
            font-family: 'Outfit', 'Poppins', sans-serif;
        }
        
        h1 {
            color: #bb86fc;
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            letter-spacing: -0.5px;
            font-size: clamp(1.5rem, 4vw, 2.5rem);
            margin-bottom: 0.5rem;
            text-shadow: 0 0 8px rgba(187, 134, 252, 0.3);
        }
        
        h2, h3 {
            color: #03dac6;
            font-family: 'Poppins', sans-serif;
            font-weight: 500;
            font-size: clamp(1.1rem, 3vw, 1.8rem);
            letter-spacing: 0.5px;
        }
        
        p {
            font-family: 'Outfit', sans-serif;
            font-size: clamp(0.95rem, 2vw, 1rem);
            line-height: 1.6;
            letter-spacing: 0.3px;
        }
        
        /* Main content container responsive padding */
        .block-container {
            padding-top: 1rem;
            padding-left: max(1rem, 5vw) !important;
            padding-right: max(1rem, 5vw) !important;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Make the chat container more friendly */
        .stChatMessage {
            border-radius: 18px;
            padding: clamp(8px, 2vw, 12px);
            margin-bottom: 14px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            max-width: 90%;
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
        }
        
        /* User message styling */
        .stChatMessage[data-testid="user-message"] {
            background-color: #292942 !important;
            border-left: 3px solid #03dac6;
            margin-left: auto;
            margin-right: 5px;
        }
        
        /* Bot message styling */
        .stChatMessage[data-testid="assistant-message"] {
            background-color: #1f1f35 !important;
            border-left: 3px solid #bb86fc;
            position: relative;
            padding-right: 45px !important;
            margin-left: 5px;
        }
        
        /* Force text color in all chat messages */
        .stChatMessage [data-testid="stMarkdownContainer"] p,
        .stChatMessage [data-testid="stMarkdownContainer"] li,
        .stChatMessage [data-testid="stMarkdownContainer"] strong,
        .stChatMessage [data-testid="stMarkdownContainer"] em,
        .stChatMessage [data-testid="stMarkdownContainer"] a,
        .stChatMessage [data-testid="stMarkdownContainer"] h1,
        .stChatMessage [data-testid="stMarkdownContainer"] h2,
        .stChatMessage [data-testid="stMarkdownContainer"] h3,
        .stChatMessage [data-testid="stMarkdownContainer"] h4,
        .stChatMessage [data-testid="stMarkdownContainer"] h5,
        .stChatMessage [data-testid="stMarkdownContainer"] h6,
        .stChatMessage [data-testid="stMarkdownContainer"] span,
        .stChatMessage [data-testid="stMarkdownContainer"] div {
            color: #e0e0ff !important;
            font-size: clamp(0.95rem, 2vw, 1rem) !important;
            font-weight: 400 !important;
            letter-spacing: 0.3px !important;
            overflow-wrap: break-word !important;
            word-wrap: break-word !important;
        }
        
        /* Chat input styling */
        .stChatInputContainer {
            padding: clamp(8px, 2vw, 12px);
            border-radius: 24px;
            border: 2px solid #03dac6;
            background-color: #1f1f35;
            box-shadow: 0 2px 15px rgba(3, 218, 198, 0.15);
            width: 100%;
            max-width: 100%;
            transition: all 0.3s ease;
        }
        
        .stChatInputContainer:focus-within {
            border-color: #bb86fc;
            box-shadow: 0 2px 15px rgba(187, 134, 252, 0.2);
        }
        
        /* Button styling */
        .stButton button {
            background-color: #03dac6;
            color: #0f0f1a;
            border-radius: 24px;
            padding: 5px 20px;
            border: none;
            font-weight: 500;
            transition: all 0.3s ease;
            width: 100%;
            font-family: 'Poppins', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.9rem;
        }
        
        .stButton button:hover {
            background-color: #bb86fc;
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(187, 134, 252, 0.2);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            flex-wrap: wrap;
            background-color: #0f0f1a;
            border-radius: 12px;
            padding: 4px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: clamp(6px, 2vw, 10px) clamp(8px, 3vw, 20px);
            background-color: #1f1f35;
            font-size: clamp(0.8rem, 1.5vw, 0.9rem);
            white-space: nowrap;
            color: #e0e0ff;
            font-weight: 500;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            font-family: 'Poppins', sans-serif;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #bb86fc !important;
            color: #0f0f1a !important;
            font-weight: 600;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #1f1f35;
            border-right: 1px solid #292942;
            padding: 20px;
            min-width: 220px !important;
            width: min(100%, 450px) !important;
        }
        
        /* Dividers */
        hr {
            border-top: 1px solid #292942;
            margin: 20px 0;
        }
        
        /* Resource card styling */
        .resource-card {
            background-color: #1f1f35;
            border-radius: 15px;
            padding: clamp(15px, 3vw, 20px);
            margin-bottom: 18px;
            border-left: 5px solid #03dac6;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            width: 100%;
            overflow-wrap: break-word;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .resource-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        }
        
        .resource-card h3 {
            color: #03dac6;
            margin-bottom: 12px;
            font-weight: 600;
            font-size: clamp(1rem, 2.5vw, 1.3rem);
        }
        
        .resource-card p {
            color: #c0c0d0;
            line-height: 1.5;
            font-size: clamp(0.85rem, 2vw, 1rem);
        }
        
        /* Positive affirmations styling */
        .affirmation {
            background-color: #292942;
            border-radius: 15px;
            padding: clamp(15px, 3vw, 20px);
            margin: 18px 0;
            border-left: 5px solid #bb86fc;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
            font-style: italic;
            color: #e0e0ff;
            font-size: clamp(0.85rem, 2vw, 1rem);
        }
        
        /* Emoji decorations */
        .emoji-heading {
            font-size: clamp(1.2rem, 3vw, 1.5rem);
            margin-right: 10px;
        }
        
        /* Warning signs styling */
        .warning-sign {
            padding: clamp(12px, 2vw, 15px);
            border-radius: 12px;
            margin-bottom: 12px;
            font-size: clamp(0.85rem, 2vw, 0.95rem);
            line-height: 1.5;
        }
        
        .warning-sign-even {
            background-color: #292942;
            color: #c0c0d0;
            border-left: 3px solid #03dac6;
        }
        
        .warning-sign-odd {
            background-color: #1f1f35;
            color: #c0c0d0;
            border-left: 3px solid #bb86fc;
        }
        
        /* Today's affirmation box */
        .daily-affirmation {
            background-color: #292942;
            padding: clamp(15px, 3vw, 20px);
            border-radius: 15px;
            margin-bottom: 24px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
            border-left: 5px solid #03dac6;
            position: relative;
            overflow: hidden;
        }
        
        .daily-affirmation::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(187, 134, 252, 0.1) 0%, rgba(3, 218, 198, 0.1) 100%);
            pointer-events: none;
        }
        
        .daily-affirmation h3 {
            color: #bb86fc;
            margin-bottom: 10px;
            font-size: clamp(1rem, 2.5vw, 1.2rem);
        }
        
        .daily-affirmation p {
            font-size: clamp(1rem, 2vw, 1.1rem);
            font-style: italic;
            color: #e0e0ff;
            line-height: 1.6;
        }
        
        /* Empty state styling */
        .empty-state {
            min-height: clamp(200px, 50vh, 300px);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: #1f1f35;
            border-radius: 20px;
            padding: 30px;
            margin: 20px 0;
            width: 100%;
            position: relative;
            overflow: hidden;
        }
        
        .empty-state::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(187, 134, 252, 0.05) 0%, rgba(3, 218, 198, 0.05) 100%);
            pointer-events: none;
        }
        
        .empty-state img {
            width: clamp(60px, 15vw, 90px);
            margin-bottom: 24px;
            opacity: 0.8;
            filter: hue-rotate(180deg) brightness(1.5);
        }
        
        .empty-state p {
            color: #c0c0d0;
            text-align: center;
            max-width: min(400px, 90%);
            font-size: clamp(0.9rem, 2vw, 1rem);
            line-height: 1.6;
        }
        
        /* Links styling */
        a {
            color: #03dac6;
            text-decoration: none;
            font-weight: 500;
            word-break: break-all;
            transition: all 0.2s ease;
        }
        
        a:hover {
            color: #bb86fc;
            text-decoration: none;
            text-shadow: 0 0 8px rgba(187, 134, 252, 0.3);
        }
        
        /* Speech button styling */
        .speech-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: #0f0f1a;
            background-color: #03dac6;
            border: none;
            border-radius: 50%;
            width: 32px;
            height: 32px;
            margin-left: 8px;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(3, 218, 198, 0.3);
            transition: all 0.3s ease;
        }
        
        .speech-button:hover {
            background-color: #bb86fc;
            transform: scale(1.1) rotate(5deg);
            box-shadow: 0 3px 10px rgba(187, 134, 252, 0.4);
        }
        
        /* Responsive layout adjustments */
        @media (max-width: 768px) {
            /* Adjust spacing for mobile */
            .block-container {
                padding-left: 10px !important;
                padding-right: 10px !important;
            }
            
            /* Stack columns on mobile */
            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                margin-bottom: 1rem;
            }
            
            /* Make sure chat container is full width */
            .stChatContainer {
                width: 100% !important;
            }
            
            /* Adjust tabs for mobile */
            .stTabs [data-baseweb="tab"] {
                padding: 6px 10px;
                font-size: 0.8rem;
            }
            
            /* Smaller emoji on mobile */
            .emoji-heading {
                font-size: 1.2rem;
            }
        }
        
        /* Medium screens adjustments */
        @media (min-width: 769px) and (max-width: 1200px) {
            /* Adjust column spacing for tablets */
            [data-testid="column"] {
                padding: 0 0.5rem !important;
            }
        }
        
        /* Ensure content doesn't overflow on any screen size */
        * {
            max-width: 100%;
            box-sizing: border-box;
        }
        
        /* Modern scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #1f1f35;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #03dac6;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #bb86fc;
        }
    </style>
    """, unsafe_allow_html=True)

    # Mobile detection function 
    def is_mobile():
        """
        Simplified function that focuses on responsive CSS rather than server-side detection.
        This avoids type errors and other platform detection issues.
        """
        # Add responsive CSS classes that will activate on the client side based on screen width
        st.markdown("""
        <style>
        .show-mobile {display: none;}
        .show-desktop {display: block;}
        @media (max-width: 768px) {
            .show-mobile {display: block;}
            .show-desktop {display: none;}
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Set a default for server-side rendering - all layout decisions 
        # will be handled by CSS on the client side
        return False

    # Responsive layout for the main content
    # Mobile-first approach
    is_on_mobile = is_mobile()

    # Mobile detection to adjust layout
    if is_on_mobile:
        # Full-width mobile-optimized layout with smaller headings
        st.markdown("<h1 style='font-size:1.8rem; text-align:center;'>☀️ Sunshine</h1>", unsafe_allow_html=True)
        st.markdown("""
        <p style="font-size: 1rem; color: #7f8c8d; text-align:center;">Mental wellness companion</p>
        """, unsafe_allow_html=True)
    else:
        # Desktop layout with normal headings
        st.markdown("# ☀️ Sunshine: Mental Wellness Companion")
        st.markdown("""
        <p style="font-size: 18px; color: #7f8c8d;">A friendly space to share, reflect, and find support</p>
        """, unsafe_allow_html=True)

    # Daily affirmation - responsive for both mobile and desktop
    today_affirmation = random.choice([
        "You are capable of amazing things, even on difficult days.",
        "Your feelings matter and deserve to be acknowledged.",
        "Small steps forward are still progress worth celebrating.",
        "You are not defined by your struggles, but by your courage to face them.",
        "Today is a new opportunity to be gentle with yourself."
    ])

    st.markdown("""
    <div class="daily-affirmation">
        <h3>✨ Today's Affirmation</h3>
        <p>"{}"</p>
    </div>
    """.format(today_affirmation), unsafe_allow_html=True)

    # Tabs for chat and resources
    tab1, tab2 = st.tabs(["💬 Chat", "🌱 Resources"])

    # Set up layout with a container for messages that takes most of the screen
    with tab1:
        # Create a container for chat history with larger height
        chat_container = st.container()
        
        # Reserve space at bottom for input
        input_container = st.container()
        
        # Display chat history in the main container
        with chat_container:
            # Adjust the top padding based on device size
            if is_on_mobile:
                st.markdown("<div style='min-height: 20px'></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='min-height: 50px'></div>", unsafe_allow_html=True)
            
            # Display messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    # Add speech button to assistant messages
                    if message["role"] == "assistant":
                        cols = st.columns([0.9, 0.1])
                        with cols[1]:
                            if st.button("🔊", key=f"speak_{hash(message['content'])}", help="Listen to this message"):
                                # Add HTML with JavaScript to speak the text
                                clean_text = message["content"].replace('"', '\\"').replace('\n', ' ')
                                st.components.v1.html(
                                    f"""
                                    <script>
                                        var utterance = new SpeechSynthesisUtterance("{clean_text}");
                                        // Gentle pace with loving warmth
                                        utterance.rate = 0.85;
                                        // Higher pitch for a softer, more affirmative tone
                                        utterance.pitch = 1.2;
                                        utterance.volume = 1.0;
                                        
                                        // Try to find voices with warm, affirming qualities
                                        window.speechSynthesis.onvoiceschanged = function() {{
                                            var voices = window.speechSynthesis.getVoices();
                                            var preferredVoices = [
                                                // Warm, affirming voice options
                                                "Google UK English Female", 
                                                "Samantha",
                                                "Karen",
                                                "Moira",
                                                "Microsoft Zira Desktop",
                                                "Microsoft Hazel Desktop",
                                                "Microsoft Susan Mobile",
                                                "Veena",
                                                "Fiona"
                                            ];
                                            
                                            // Try preferred voices first
                                            for(var i = 0; i < preferredVoices.length; i++) {{
                                                var voice = voices.find(v => v.name.includes(preferredVoices[i]));
                                                if(voice) {{
                                                    utterance.voice = voice;
                                                    break;
                                                }}
                                            }}
                                            
                                            // If no preferred voice found, try to use any available female voice
                                            if(!utterance.voice) {{
                                                var femaleVoice = voices.find(v => 
                                                    v.name.includes('Female') || 
                                                    v.name.includes('female') || 
                                                    v.name.includes('woman') ||
                                                    v.name.includes('Girl')
                                                );
                                                if(femaleVoice) utterance.voice = femaleVoice;
                                            }}
                                            
                                            // Speak with the selected voice
                                            window.speechSynthesis.speak(utterance);
                                        }};
                                        
                                        // Ensure voices are loaded
                                        if (window.speechSynthesis.getVoices().length > 0) {{
                                            window.speechSynthesis.onvoiceschanged();
                                        }} else {{
                                            // Directly try to speak if voices are already loaded
                                            window.speechSynthesis.speak(utterance);
                                        }}
                                    </script>
                                    """,
                                    height=0
                                )
        
        # Add extra space to push content up if few messages
        if len(st.session_state.messages) < 2:
            st.markdown("""
            <div class="empty-state">
                <img src="https://img.icons8.com/clouds/100/000000/chat.png">
                <p>Share what's on your mind, and I'm here to listen and support you on your mental wellness journey.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Process input at bottom with responsive design
    with input_container:
        prompt = st.chat_input("Share what's on your mind...", key="chat_input")
        
        if prompt:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Check for crisis keywords
            is_crisis, crisis_type = check_for_crisis_keywords(prompt)
            if is_crisis:
                # Update crisis detection flag
                st.session_state.conversation_state["crisis_detected"] = True
                
                if crisis_type == "self_harm":
                    # Prepare suicide/self-harm crisis response
                    # First a compassionate validation
                    crisis_validation = get_unique_response("crisis_support", RESPONSES["crisis_support"])
                    
                    # Add an affirmation
                    affirmation = get_unique_response("affirmations", RESPONSES["affirmations"])
                    
                    # Explicit crisis resources
                    crisis_resources = """
                    **Crisis Resources:**
                    - National Suicide Prevention Lifeline: 988 or 1-800-273-8255
                    - Crisis Text Line: Text HOME to 741741
                    
                    These services are available 24/7 and provide confidential support from trained counselors.
                    """
                    
                    # Combine all parts
                    crisis_message = f"{crisis_validation}\n\n{affirmation}\n\n{crisis_resources}"
                
                elif crisis_type == "violent_thoughts":
                    # Analyze the severity and intent
                    anger_level = analyze_anger_level(prompt)
                    
                    if anger_level == "critical":
                        # Handle urgent or explicit violent thoughts
                        crisis_validation = get_unique_response("violent_thoughts_critical", RESPONSES["violent_thoughts_critical"])
                    elif anger_level == "venting":
                        # Handle angry venting
                        crisis_validation = get_unique_response("violent_thoughts_venting", RESPONSES["violent_thoughts_venting"])
                    else:
                        # Handle processing/exploring
                        crisis_validation = get_unique_response("violent_thoughts_processing", RESPONSES["violent_thoughts_processing"])
                    
                    # Add an affirmation
                    affirmation = get_unique_response("affirmations", RESPONSES["affirmations"])
                    
                    # Provide appropriate resources
                    crisis_resources = RESPONSES["safety_resources"][0]
                    
                    # Combine all parts
                    crisis_message = f"{crisis_validation}\n\n{affirmation}\n\n{crisis_resources}"
                
                # Add to chat history
                st.session_state.messages.append({"role": "assistant", "content": crisis_message})
            else:
                # Track topics mentioned for future reference
                detect_and_store_topics(prompt)
                
                # Generate normal response
                response = get_response(prompt)
                
                # Add to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Rerun to show the new messages without moving input field
            st.rerun()

    with tab2:
        # Resource tabs with emojis - simplified for mobile
        if is_on_mobile:
            resource_tab1, resource_tab2 = st.tabs(["🆘 Crisis", "🧠 Support"])
            
            with resource_tab1:
                st.markdown("<h2 style='color: #1e88e5;'><span style='font-size: 24px;'>🆘</span> Crisis Resources</h2>", unsafe_allow_html=True)
                st.markdown("<p>Everyone needs help sometimes. Reaching out is a sign of strength.</p>", unsafe_allow_html=True)
                
                st.markdown("<h3 style='color: #1e88e5;'>United States</h3>", unsafe_allow_html=True)
                for resource in CRISIS_RESOURCES["united_states"]:
                    resource_card(
                        resource['name'], 
                        f"""
                        <p><strong>Phone:</strong> {resource.get('phone', 'N/A')}</p>
                        {"<p><strong>Text:</strong> " + resource['text'] + "</p>" if 'text' in resource else ""}
                        <p><strong>Website:</strong> <a href="{resource['website']}" target="_blank">{resource['website']}</a></p>
                        <p><em>{resource['description']}</em></p>
                        """,
                        emoji="📞"
                    )
                
                st.markdown("<h3 style='color: #1e88e5;'>Global</h3>", unsafe_allow_html=True)
                for resource in CRISIS_RESOURCES["global"]:
                    resource_card(
                        resource['name'],
                        f"""
                        <p><strong>Website:</strong> <a href="{resource['website']}" target="_blank">{resource['website']}</a></p>
                        <p><em>{resource['description']}</em></p>
                        """,
                        emoji="🌎"
                    )
            
            with resource_tab2:
                # Combined tab for all non-crisis resources on mobile
                st.markdown("<h2 style='color: #1e88e5;'><span style='font-size: 24px;'>🧠</span> Coping Strategies</h2>", unsafe_allow_html=True)
                
                # Show key strategies for each category
                for category, strategies in COPING_STRATEGIES.items():
                    emoji_map = {
                        "anxiety": "😌",
                        "depression": "🌤️",
                        "stress": "🧘",
                        "sleep": "😴",
                        "anger": "🧠"
                    }
                    emoji = emoji_map.get(category.lower(), "💡")
                    
                    resource_card(
                        f"For {category.title()}",
                        "".join([f"<p>• {strategy}</p>" for strategy in strategies[:2]]),  # Show fewer strategies on mobile
                        emoji=emoji
                    )
                
                # Self-care section
                st.markdown("<h2 style='color: #1e88e5;'><span style='font-size: 24px;'>🌸</span> Self-Care</h2>", unsafe_allow_html=True)
                st.markdown("<p>Taking care of yourself isn't selfish—it's necessary.</p>", unsafe_allow_html=True)
                
                # Show fewer reminders on mobile
                for reminder in SELF_CARE_REMINDERS[:4]:
                    display_affirmation(reminder)
                    
                # Warning signs - fewer on mobile
                st.markdown("<h2 style='color: #1e88e5;'><span style='font-size: 24px;'>⚠️</span> Warning Signs</h2>", unsafe_allow_html=True)
                
                for i, sign in enumerate(WARNING_SIGNS[:5]):
                    odd_even_class = "warning-sign-even" if i % 2 == 0 else "warning-sign-odd"
                    
                    st.markdown(f"""
                    <div class="warning-sign {odd_even_class}">
                        • {sign}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            # Full tabs layout for desktop/tablet
            resource_tab1, resource_tab2, resource_tab3, resource_tab4 = st.tabs([
                "🆘 Crisis Resources", "🧠 Coping Strategies", "🌸 Self-Care", "⚠️ Warning Signs"
            ])
            
            with resource_tab1:
                st.markdown("<h2 style='color: #1e88e5;'><span style='font-size: 30px;'>🆘</span> Crisis Resources</h2>", unsafe_allow_html=True)
                st.markdown("<p>Everyone needs help sometimes. Reaching out is a sign of strength.</p>", unsafe_allow_html=True)
                
                st.markdown("<h3 style='color: #1e88e5;'>United States</h3>", unsafe_allow_html=True)
                for resource in CRISIS_RESOURCES["united_states"]:
                    resource_card(
                        resource['name'], 
                        f"""
                        <p><strong>Phone:</strong> {resource.get('phone', 'N/A')}</p>
                        {"<p><strong>Text:</strong> " + resource['text'] + "</p>" if 'text' in resource else ""}
                        <p><strong>Website:</strong> <a href="{resource['website']}" target="_blank">{resource['website']}</a></p>
                        <p><em>{resource['description']}</em></p>
                        """,
                        emoji="📞"
                    )
                
                st.markdown("<h3 style='color: #1e88e5;'>Global</h3>", unsafe_allow_html=True)
                for resource in CRISIS_RESOURCES["global"]:
                    resource_card(
                        resource['name'],
                        f"""
                        <p><strong>Website:</strong> <a href="{resource['website']}" target="_blank">{resource['website']}</a></p>
                        <p><em>{resource['description']}</em></p>
                        """,
                        emoji="🌎"
                    )
            
            with resource_tab2:
                st.markdown("<h2 style='color: #1e88e5;'><span style='font-size: 30px;'>🧠</span> Coping Strategies</h2>", unsafe_allow_html=True)
                st.markdown("<p>Small tools can make a big difference when facing challenges.</p>", unsafe_allow_html=True)
                
                for category, strategies in COPING_STRATEGIES.items():
                    emoji_map = {
                        "anxiety": "😌",
                        "depression": "🌤️",
                        "stress": "🧘",
                        "sleep": "😴",
                        "anger": "🧠"
                    }
                    emoji = emoji_map.get(category.lower(), "💡")
                    
                    resource_card(
                        f"For {category.title()}",
                        "".join([f"<p>• {strategy}</p>" for strategy in strategies]),
                        emoji=emoji
                    )
            
            with resource_tab3:
                st.markdown("<h2 style='color: #1e88e5;'><span style='font-size: 30px;'>🌸</span> Self-Care Reminders</h2>", unsafe_allow_html=True)
                st.markdown("<p>Taking care of yourself isn't selfish—it's necessary.</p>", unsafe_allow_html=True)
                
                # Create two columns for self-care items
                col1, col2 = st.columns(2)
                
                # Split reminders between columns
                half = len(SELF_CARE_REMINDERS) // 2
                
                with col1:
                    for reminder in SELF_CARE_REMINDERS[:half]:
                        display_affirmation(reminder)
                
                with col2:
                    for reminder in SELF_CARE_REMINDERS[half:]:
                        display_affirmation(reminder)
            
            with resource_tab4:
                st.markdown("<h2 style='color: #1e88e5;'><span style='font-size: 30px;'>⚠️</span> Warning Signs</h2>", unsafe_allow_html=True)
                st.markdown("<p>When to consider reaching out to a mental health professional:</p>", unsafe_allow_html=True)
                
                # Create a visually appealing list of warning signs
                for i, sign in enumerate(WARNING_SIGNS):
                    odd_even_class = "warning-sign-even" if i % 2 == 0 else "warning-sign-odd"
                    
                    st.markdown(f"""
                    <div class="warning-sign {odd_even_class}">
                        • {sign}
                    </div>
                    """, unsafe_allow_html=True)

    # Sidebar with important information and session info
    with st.sidebar:
        # Removed all content from sidebar as requested
        pass

    # Disclaimer removed 