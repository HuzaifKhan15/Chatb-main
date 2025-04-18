"""
Mental health resources and information for the counseling chatbot.
These can be referenced by the main application.
"""

# Crisis resources
CRISIS_RESOURCES = {
    "global": [
        {
            "name": "International Association for Suicide Prevention",
            "website": "https://www.iasp.info/resources/Crisis_Centres/",
            "description": "Directory of crisis centers around the world"
        },
    ],
    "united_states": [
        {
            "name": "National Suicide Prevention Lifeline",
            "phone": "988 or 1-800-273-8255",
            "website": "https://suicidepreventionlifeline.org/",
            "description": "24/7 free and confidential support for people in distress"
        },
        {
            "name": "Crisis Text Line",
            "text": "HOME to 741741",
            "website": "https://www.crisistextline.org/",
            "description": "Text-based crisis support available 24/7"
        },
        {
            "name": "SAMHSA's National Helpline",
            "phone": "1-800-662-4357",
            "website": "https://www.samhsa.gov/find-help/national-helpline",
            "description": "Treatment referral and information service (in English and Spanish)"
        },
    ]
}

# Common coping strategies
COPING_STRATEGIES = {
    "anxiety": [
        "Deep breathing exercises: Breathe in for 4 counts, hold for 2, and exhale for 6",
        "Progressive muscle relaxation: Tense and release each muscle group",
        "Grounding techniques: Name 5 things you can see, 4 things you can touch, 3 things you can hear, 2 things you can smell, and 1 thing you can taste",
        "Limit caffeine and alcohol consumption",
        "Regular physical exercise",
        "Mindfulness meditation"
    ],
    "depression": [
        "Establish a consistent daily routine",
        "Set small, achievable goals for yourself",
        "Physical activity, even if just a short walk",
        "Connect with supportive friends or family",
        "Practice self-compassion and challenge negative thoughts",
        "Engage in activities that previously brought joy, even if motivation is low"
    ],
    "stress": [
        "Time management and prioritization of tasks",
        "Setting boundaries with work and relationships",
        "Regular relaxation practices like yoga or tai chi",
        "Ensuring adequate sleep",
        "Journaling to process thoughts and emotions",
        "Engaging in creative activities"
    ]
}

# Self-care reminders
SELF_CARE_REMINDERS = [
    "Remember to drink water regularly throughout the day",
    "Try to get 7-9 hours of sleep each night",
    "Take short breaks throughout your day to reset",
    "Spend some time outdoors to boost your mood",
    "Move your body in ways that feel good to you",
    "Practice gratitude by noting three positive things each day",
    "Set boundaries with technology and social media",
    "Connect with someone who supports you",
    "Engage in an activity solely because you enjoy it"
]

# Warning signs that indicate need for professional help
WARNING_SIGNS = [
    "Thoughts of harming yourself or others",
    "Feeling hopeless or that life isn't worth living",
    "Significant changes in sleep, appetite, or energy levels",
    "Withdrawal from friends, family, and normal activities",
    "Difficulty functioning at work, school, or in relationships",
    "Overwhelming anxiety, fear, or panic attacks",
    "Mood swings that cause problems in relationships",
    "Increased use of substances to cope",
    "Significant changes in behavior or personality"
] 