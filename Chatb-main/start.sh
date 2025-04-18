#!/bin/bash

echo "Starting Mental Health Counseling Chatbot..."
echo ""
echo "Please make sure you've set your Google API key in the .env file!"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in your PATH."
    echo "Please install Python from https://www.python.org/downloads/"
    exit 1
fi

# Check if requirements are installed
echo "Checking for required packages..."
pip install -r requirements.txt

# Start the Streamlit app
echo ""
echo "Starting the application..."
streamlit run app.py 