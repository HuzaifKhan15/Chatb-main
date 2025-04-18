@echo off
echo Starting Mental Health Counseling Chatbot...
echo.
echo Please make sure you've set your Google API key in the .env file!
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in your PATH.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b
)

REM Check if requirements are installed
echo Checking for required packages...
pip install -r requirements.txt

REM Start the Streamlit app
echo.
echo Starting the application...
streamlit run app.py

pause 