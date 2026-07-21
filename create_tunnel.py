"""
Creates a public URL tunnel to localhost:8000 using serveo.net or localhost.run.
No signup required. The FastAPI server must already be running on port 8000.
"""
import subprocess
import re
import sys
import time
import os
import threading
import json

URL_FILE = "public_url.txt"

def try_serveo():
    """Try serveo.net tunnel."""
    print("[*] Trying serveo.net tunnel...")
    cmd = [
        "ssh", "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=30",
        "-R", "80:localhost:8000",
        "serveo.net"
    ]
    return start_tunnel(cmd, "serveo.net")

def try_localhost_run():
    """Try localhost.run tunnel."""
    print("[*] Trying localhost.run tunnel...")
    cmd = [
        "ssh", "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=30",
        "-R", "80:localhost:8000",
        "nokey@localhost.run"
    ]
    return start_tunnel(cmd, "localhost.run")

def start_tunnel(cmd, service_name):
    """Start an SSH tunnel and extract the public URL."""
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        errors='replace'
    )

    url = None
    url_patterns = [
        re.compile(r'(https?://[a-zA-Z0-9][-a-zA-Z0-9]*\.' + service_name.replace('.', r'\.') + r')'),
        re.compile(r'([a-zA-Z0-9][-a-zA-Z0-9]*\.' + service_name.replace('.', r'\.') + r')'),
    ]

    # Read in thread
    lines = []
    stop = threading.Event()

    def reader():
        for line in iter(proc.stdout.readline, ''):
            if stop.is_set():
                break
            line_clean = line.strip()
            if line_clean:
                lines.append(line_clean)
                print(f"  {line_clean[:200]}")
                sys.stdout.flush()

    t = threading.Thread(target=reader, daemon=True)
    t.start()

    # Wait for URL (up to 30 seconds)
    for i in range(30):
        for line in lines:
            line_lower = line.lower()
            for pattern in url_patterns:
                m = pattern.search(line)
                if m:
                    raw = m.group(1)
                    if not raw.startswith('http'):
                        raw = 'https://' + raw
                    skip_words = ['admin', 'console', 'dashboard']
                    if not any(w in raw for w in skip_words):
                        url = raw
                        break
            if url:
                break
        if url:
            break
        time.sleep(1)

    if url:
        stop.set()
        return url, proc

    # Timeout - kill and return None
    stop.set()
    proc.terminate()
    return None, None

def print_info(url):
    """Print access information."""
    print()
    print("=" * 70)
    print(f"  PUBLIC URL: {url}")
    print("=" * 70)
    print()
    print(f"  Share this link: {url}")
    print()
    print("  Available pages:")
    for path, desc in [
        ("", "Home (Login page)"),
        ("/dashboard", "Dashboard"),
        ("/tracker", "Tracker"),
        ("/map", "Map Tracker"),
        ("/live", "Live Visibility"),
        ("/operations", "Operations"),
        ("/health", "Health Check"),
        ("/docs", "API Docs (Swagger)"),
    ]:
        print(f"    {url}{path:15s} -> {desc}")
    print()
    print("  Default login credentials:")
    print("    Username: admin")
    print("    Password: admin123")
    print()
    print("  Press Ctrl+C to stop the tunnel.")

def main():
    print("=" * 70)
    print("  Creating public URL for your Logistics App")
    print("  (Server should be running on localhost:8000)")
    print("=" * 70)
    print()

    # Check server is running
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", 8000))
        s.close()
        print("[OK] Server is running on port 8000")
    except:
        print("[WARN] Cannot connect to port 8000. Make sure the server is running.")
        print("  Start with: .venv\\Scripts\\uvicorn app.main:app --host 0.0.0.0 --port 8000")
        print()

    # Try serveo first, then localhost.run
    url = None
    proc = None

    url, proc = try_serveo()
    if not url:
        print("[!] serveo.net failed, trying localhost.run...")
        url, proc = try_localhost_run()

    if url:
        # Save URL
        with open(URL_FILE, "w") as f:
            f.write(url)
        print_info(url)
    else:
        print()
        print("[ERROR] Could not create tunnel.")
        print("  Possible issues:")
        print("  - SSH is not installed or configured")
        print("  - Firewall blocking outbound SSH connections")
        print("  - The tunnel services may be down")
        print()
        print("  Alternative: Deploy to a cloud service like Render, Railway, or PythonAnywhere")
        return

    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Stopping tunnel...")
        if proc:
            proc.terminate()
        print("[OK] Tunnel closed.")

if __name__ == "__main__":
    main()

