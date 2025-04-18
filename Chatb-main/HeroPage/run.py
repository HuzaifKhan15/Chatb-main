import os
import subprocess
import sys

# Get the absolute path of the current script directory
current_dir = os.path.dirname(os.path.abspath(__file__))
main_app_path = os.path.join(current_dir, "main.py")

# Run the Streamlit app
print("Starting Sunshine Mental Wellness Portal...")
subprocess.run([sys.executable, "-m", "streamlit", "run", main_app_path]) 