import os
import json
from datetime import datetime
import random
from resources import (
    CRISIS_RESOURCES,
    COPING_STRATEGIES,
    SELF_CARE_REMINDERS,
    WARNING_SIGNS
)
from app import (
    check_for_crisis_keywords,
    detect_issue,
    detect_conversation_type,
    extract_name,
    extract_emotions
)

# Advanced conversation templates
CONVERSATION_STARTERS = {
    "greeting": [
        "Hey, how are you feeling today?",
        "Hi there! What's on your mind?",
        "Hello! I'm here to listen. What would you like to talk about?",
        "Hey! How's your day going?",
        "Hi! What brings you here today?"
    ],
    "follow_up": [
        "Tell me more about that.",
        "How does that make you feel?",
        "What thoughts come up when you think about this?",
        "When did you first notice this?",
        "How long have you been feeling this way?"
    ],
    "validation": [
        "That sounds really challenging.",
        "I hear how difficult this is for you.",
        "Your feelings are completely valid.",
        "That's a lot to deal with.",
        "It makes sense that you'd feel this way."
    ],
    "transition": [
        "I'm curious to know more about...",
        "Speaking of which...",
        "That reminds me...",
        "On a related note...",
        "While we're talking about this..."
    ]
}

def create_natural_conversation(input_text, response_type, context=None):
    """Create more natural conversation flows with varied responses"""
    conversation = []
    
    # Add greeting
    conversation.append({
        "input": input_text,
        "response": random.choice(CONVERSATION_STARTERS["greeting"]),
        "type": "greeting"
    })
    
    # Add contextual response
    if context:
        conversation.append({
            "input": f"I'm feeling {context}",
            "response": random.choice(CONVERSATION_STARTERS["validation"]),
            "type": "validation"
        })
    
    # Add follow-up
    conversation.append({
        "input": "I just need someone to talk to",
        "response": random.choice(CONVERSATION_STARTERS["follow_up"]),
        "type": "follow_up"
    })
    
    return conversation

def create_training_data():
    """Create a comprehensive training dataset from all available resources"""
    training_data = []
    
    # Add natural conversations
    emotions = ["anxious", "sad", "overwhelmed", "stressed", "lonely", "confused"]
    for emotion in emotions:
        training_data.extend(create_natural_conversation(
            f"I'm feeling {emotion}",
            "emotional_support",
            emotion
        ))
    
    # Add crisis scenarios with more natural language
    for region, resources in CRISIS_RESOURCES.items():
        for resource in resources:
            variations = [
                f"I need help with {resource['name']}",
                f"Can you tell me about {resource['name']}?",
                f"I'm looking for support from {resource['name']}",
                f"Where can I find {resource['name']}?"
            ]
            for variation in variations:
                training_data.append({
                    "input": variation,
                    "response": f"I understand you need help with {resource['name']}. {resource['description']} You can reach them at {resource.get('website', 'their website')}.",
                    "type": "crisis",
                    "region": region
                })
    
    # Add coping strategies with conversational context
    for issue, strategies in COPING_STRATEGIES.items():
        for strategy in strategies:
            variations = [
                f"I'm struggling with {issue}",
                f"How can I deal with {issue}?",
                f"I need help managing my {issue}",
                f"What can I do about my {issue}?"
            ]
            for variation in variations:
                training_data.append({
                    "input": variation,
                    "response": f"For {issue}, here's a helpful strategy: {strategy}",
                    "type": "coping",
                    "issue": issue
                })
                # Add follow-up response
                training_data.append({
                    "input": f"Tell me more about {strategy}",
                    "response": f"Let me explain this strategy in more detail. {strategy} This can help you manage {issue} by providing a practical tool you can use when you're feeling overwhelmed.",
                    "type": "coping_detail",
                    "issue": issue
                })
    
    # Add self-care reminders with natural transitions
    for reminder in SELF_CARE_REMINDERS:
        variations = [
            "I need to take better care of myself",
            "How can I practice self-care?",
            "I'm feeling burnt out",
            "I need some self-care tips"
        ]
        for variation in variations:
            training_data.append({
                "input": variation,
                "response": f"Here's a gentle reminder for self-care: {reminder}",
                "type": "self_care"
            })
            # Add follow-up about implementation
            training_data.append({
                "input": f"How can I start with {reminder}?",
                "response": f"Let's break this down into manageable steps. Start small and be patient with yourself. {reminder} Remember, self-care is a journey, not a destination.",
                "type": "self_care_implementation"
            })
    
    # Add warning signs with empathetic responses
    for sign in WARNING_SIGNS:
        variations = [
            f"I've been experiencing {sign.lower()}",
            f"I'm worried about {sign.lower()}",
            f"Can you tell me more about {sign.lower()}?",
            f"What does it mean if I'm {sign.lower()}?"
        ]
        for variation in variations:
            training_data.append({
                "input": variation,
                "response": f"I hear your concern about {sign.lower()}. This could be a sign that it's time to reach out to a mental health professional. They can help you understand what's happening and provide appropriate support.",
                "type": "warning_sign"
            })
    
    return training_data

def save_training_data(training_data, filename="trained_chatbot_data.json"):
    """Save the training data to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            "training_data": training_data,
            "timestamp": datetime.now().isoformat(),
            "version": "1.0"
        }, f, indent=2, ensure_ascii=False)
    print(f"Training data saved to {filename}")

def main():
    """Main function to create and save training data"""
    print("Creating training dataset...")
    training_data = create_training_data()
    print(f"Generated {len(training_data)} training examples")
    print("Saving training data...")
    save_training_data(training_data)
    print("Training completed successfully!")

if __name__ == "__main__":
    main() 