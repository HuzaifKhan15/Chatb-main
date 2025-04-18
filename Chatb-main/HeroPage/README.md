# Sunshine Mental Wellness Portal

A Gen Z-oriented mental health portal with sign-in/login functionality that connects to a mental health chatbot.

## Features

- **User Authentication**: Secure signup and login system
- **Doctor Connection**: UI for connecting with mental health professionals
- **AI Counselor**: Integration with the Sunshine mental health chatbot
- **Modern UI**: Gen Z aesthetic with dark mode and vibrant colors

## Setup Instructions

1. Install required packages:
   ```
   pip install -r ../requirements.txt
   ```

2. Run the application:
   ```
   python run.py
   ```
   
   Or from the root directory:
   ```
   python run_portal.py
   ```
   
   Or simply double-click the `launch_portal.bat` file (Windows only)

## Default Login

For testing purposes, you can use the default admin account:
- Username: admin
- Password: admin123

## File Structure

- `main.py`: The main application with authentication and navigation
- `run.py`: Helper script to launch the application
- `config/`: Directory containing user configuration data
  - `config.yaml`: User credentials and authentication settings

## User Guide

1. **Sign Up / Login**: Create a new account or log in with existing credentials
2. **Home Page**: Choose between connecting with a doctor or chatting with the AI counselor
3. **Your Doctor**: View and connect with mental health professionals
4. **AI Counselor**: Access the Sunshine mental health chatbot

## Integration with Chatbot

The portal launches the existing chatbot application (`app.py`) as a separate process. In a production environment, you would want to modify the chatbot to be properly integrated as a module within the main application.

## Customization

- Modify the CSS in `main.py` to change the look and feel
- Add additional functionality to the doctor profiles
- Enhance the user profile and settings management

## Security Notes

- User passwords are hashed using bcrypt
- Session authentication is handled by cookies with a 30-day expiration
- Configuration file is stored locally and should be properly secured in production 