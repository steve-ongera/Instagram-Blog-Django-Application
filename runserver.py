import os
import subprocess
import webbrowser
import time

if __name__ == "__main__":
    # Change directory to where manage.py is located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Start the Django development server in a new subprocess
    subprocess.Popen(["python", "manage.py", "runserver"])

    # Give the server a moment to start
    time.sleep(5)

    # Open the default web browser to the specified URL
    webbrowser.open("http://127.0.0.1:8000")  # Adjust the URL if needed
