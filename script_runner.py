import click
import requests
import subprocess
import sys

@click.command()
@click.argument('url')
def run(url):
    """Run a Python or Bash script from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text

        if url.endswith('.py'):
            # Run Python script
            exec(content)
        elif url.endswith('.sh'):
            # Run Bash script
            result = subprocess.run(['bash', '-c', content], capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
        else:
            print(f"Unsupported file type. URL must end with .py or .sh")

    except requests.RequestException as e:
        print(f"Error fetching the script: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Error running the script: {e}", file=sys.stderr)

if __name__ == '__main__':
    run()
