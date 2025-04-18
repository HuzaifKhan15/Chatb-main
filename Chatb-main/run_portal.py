import os
import subprocess
import sys

# Get the absolute path to the HeroPage run script
current_dir = os.path.dirname(os.path.abspath(__file__))
hero_run_script = os.path.join(current_dir, "HeroPage", "run.py")

print("Starting Sunshine Mental Wellness Portal...")
subprocess.run([sys.executable, hero_run_script]) 