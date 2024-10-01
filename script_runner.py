import sys
import subprocess
import argparse
import urllib.request
import tempfile
import os

VERSION = "1.0.1"

def is_url(string):
    return string.startswith(('http://', 'https://'))

def download_script(url):
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.py') as temp_file:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')
            temp_file.write(content)
        return temp_file.name

def main():
    parser = argparse.ArgumentParser(description="Run a Python script or shell script from file or URL with arguments.")
    parser.add_argument("script_name", help="The name of the script to run or its URL")
    parser.add_argument("script_args", nargs=argparse.REMAINDER, help="Arguments to pass to the script")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {VERSION}")
    args = parser.parse_args()

    try:
        if is_url(args.script_name):
            script_path = download_script(args.script_name)
            command = ["python", script_path] + args.script_args
        else:
            script_path = args.script_name
            if script_path.endswith('.py'):
                command = ["python", script_path] + args.script_args
            else:
                command = ["bash", script_path] + args.script_args

        subprocess.run(command, check=True)

        if is_url(args.script_name):
            os.unlink(script_path)  # Remove the temporary file

    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
