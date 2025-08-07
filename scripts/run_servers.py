import subprocess
import time


def main():
    """
    Runs the API and DNS servers concurrently.
    """
    api_command = [
        "uv",
        "run",
        "uvicorn",
        "llm_radio.api_server:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
    ]
    dns_command = ["uv", "run", "python", "src/llm_radio/dns_server.py"]

    print("Starting API server...")
    api_process = subprocess.Popen(api_command)

    print("Starting DNS server...")
    dns_process = subprocess.Popen(dns_command)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping servers...")
        api_process.terminate()
        dns_process.terminate()
        api_process.wait()
        dns_process.wait()
        print("Servers stopped.")


if __name__ == "__main__":
    main()
