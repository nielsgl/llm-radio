import os
import pty
import select
import subprocess


def run_servers():
    """
    Runs the API and DNS servers concurrently using pseudo-terminals (ptys)
    to preserve colorized output.
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

    masters = {}
    processes = {}

    for name, command in [("api", api_command), ("dns", dns_command)]:
        master, slave = pty.openpty()
        proc = subprocess.Popen(command, stdout=slave, stderr=slave)
        os.close(slave)
        masters[master] = name
        processes[name] = proc

    print("[cli] [INFO] Starting API and DNS servers...")

    try:
        while masters:
            readable, _, _ = select.select(masters.keys(), [], [], 0.1)
            for master in readable:
                try:
                    data = os.read(master, 1024)
                    if not data:
                        # Process has finished
                        masters.pop(master)
                        continue
                    prefix = f"[{masters[master]}] ".encode()
                    os.write(1, prefix + data.replace(b"\n", b"\n" + prefix)[: -len(prefix)])
                except OSError:
                    masters.pop(master)
    except KeyboardInterrupt:
        print("\n[cli] [INFO] Stopping servers...")
    finally:
        for proc in processes.values():
            proc.terminate()
        for proc in processes.values():
            proc.wait()
        print("[cli] [INFO] Servers stopped.")
