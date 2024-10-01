import sys
import subprocess
import argparse
import urllib.request
import tempfile
import os
import logging
import threading

VERSION = "1.0.2"

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def is_url(string):
    return string.startswith(('http://', 'https://'))

def download_script(url):
    suffix = '.py' if url.endswith('.py') else '.sh'
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=suffix) as temp_file:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')
            temp_file.write(content)
        logging.debug(f"Downloaded script from {url} to {temp_file.name}")
        return temp_file.name

def run_script(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Run a Python script or shell script from file or URL with arguments.")
    parser.add_argument("script_name", help="The name of the script to run or its URL")
    parser.add_argument("script_args", nargs=argparse.REMAINDER, help="Arguments to pass to the script")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {VERSION}")
    args = parser.parse_args()

    try:
        if is_url(args.script_name):
            script_path = download_script(args.script_name)
            if script_path.endswith('.py'):
                command = ["python", script_path] + args.script_args
            else:
                command = ["bash", script_path] + args.script_args
        else:
            script_path = args.script_name
            if script_path.endswith('.py'):
                command = ["python", script_path] + args.script_args
            else:
                command = ["bash", script_path] + args.script_args

        logging.debug(f"Executing command: {' '.join(command)}")
        
        # Run the script in a separate thread
        script_thread = threading.Thread(target=run_script, args=(command,))
        script_thread.start()

        # Get and print the PID
        pid = os.getpid()
        print(f"Script running in thread. Process ID: {pid}")

        # Wait for the thread to complete
        script_thread.join()

        print(f"Script execution completed.")

        if is_url(args.script_name):
            logging.debug(f"Removing temporary file: {script_path}")
            os.unlink(script_path)  # Remove the temporary file

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
