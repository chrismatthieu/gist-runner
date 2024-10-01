import sys
import subprocess
import argparse

VERSION = "1.0.0"

def main():
    parser = argparse.ArgumentParser(description="Run a Python script with arguments.")
    parser.add_argument("script_name", help="The name of the script to run")
    parser.add_argument("script_args", nargs=argparse.REMAINDER, help="Arguments to pass to the script")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {VERSION}")
    args = parser.parse_args()

    try:
        subprocess.run(["python", args.script_name] + args.script_args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
