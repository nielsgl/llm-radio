import subprocess
import sys
import threading
import time


def log_stream(stream, prefix):
    """Reads a stream line by line and prints it with a prefix."""
    for line in iter(stream.readline, ""):
        sys.stdout.write(f"[{prefix}] {line}")
    stream.close()


def run_servers():
    """
    Runs the API and DNS servers concurrently, capturing and prefixing their logs.
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

    print("[cli] Starting API server...")
    api_process = subprocess.Popen(
        api_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    print("[cli] Starting DNS server...")
    dns_process = subprocess.Popen(
        dns_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # Start threads to log the output from each process
    threading.Thread(target=log_stream, args=(api_process.stdout, "api")).start()
    threading.Thread(target=log_stream, args=(api_process.stderr, "api")).start()
    threading.Thread(target=log_stream, args=(dns_process.stdout, "dns")).start()
    threading.Thread(target=log_stream, args=(dns_process.stderr, "dns")).start()

    try:
        while api_process.poll() is None and dns_process.poll() is None:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[cli] Stopping servers...")
    finally:
        api_process.terminate()
        dns_process.terminate()
        api_process.wait()
        dns_process.wait()
        print("[cli] Servers stopped.")
