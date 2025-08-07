import subprocess
import time


def run_servers():
    """
    Runs the API and DNS servers concurrently.
    """
    api_command = [
        "uvicorn",
        "llm_radio.api_server:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
    ]
    dns_command = ["python", "-m", "llm_radio.dns_server"]

    print("Starting API server...")
    # We don't need `uv run` here because the script itself is run via `uv run`,
    # so it's already in the correct environment.
    api_process = subprocess.Popen(api_command)

    print("Starting DNS server...")
    dns_process = subprocess.Popen(dns_command)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers...")
        api_process.terminate()
        dns_process.terminate()
        api_process.wait()
        dns_process.wait()
        print("Servers stopped.")
