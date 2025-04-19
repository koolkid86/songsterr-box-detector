import os
import sys
import subprocess
import time

def run_app():
    # Get the directory of this script
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the main application
    app_path = os.path.join(app_dir, "songsterr_app.py")
    
    # Make sure we're in the right directory
    os.chdir(app_dir)
    
    # Run the application directly
    # This is more reliable than using subprocess
    import songsterr_app
    songsterr_app.main()

if __name__ == "__main__":
    run_app()