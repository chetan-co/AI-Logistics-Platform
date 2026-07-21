"""
Create a public URL using serveo.net SSH tunnel.
Simple, no signup required.
"""
import subprocess
import re
import sys
import os
import threading
import time

URL_FILE = "public_url.txt"

def read_output(proc, url_holder):
    """Read output and extract URL."""
    for line in iter(proc.stdout.readline, ""):
        line = line.strip()
        if line:
            print(line)
            sys.stdout.flush()
            # Look for URL patterns
            for pattern in [r"(https?://[a-zA-Z0-9][-a-zA-Z0-9]*\.serveo\.net)",
                            r"([a-zA-Z0-9][-a-zA-Z0-9]*\.serveo\.net)"]:
                m = re.search(pattern, line)
                if m:
                    raw = m.group(1)
                    if not raw.startswith("http"):
                        raw = "https://" + raw
                    url_holder["url"] = raw
                    return

def main():
    print("=" * 60)
    print("  Creating public URL via serveo.net tunnel")
    print("=" * 60)

    # Use autossh or plain ssh
    cmd = [
        "ssh", "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=30",
        "-R", "80:localhost:8000",
        "serveo.net"
    ]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    url_holder = {}
    reader = threading.Thread(target=read_output, args=(proc, url_holder), daemon=True)
    reader.start()

    # Wait for URL
    timeout = 20
    for i in range(timeout):
        if url_holder.get("url"):
            break
        time.sleep(1)

    url = url_holder.get("url")

    if url:
        print("\n" + "=" * 60)
        print("  PUBLIC URL: " + url)
        print("=" * 60)
        with open(URL_FILE, "w") as f:
            f.write(url)
        
        print("\n  ShARE THIS URL: " + url)
        print("\n  Available pages:")
        print("    " + url + "           -> Home")
        print("    " + url + "/dashboard  -> Dashboard")
        print("    " + url + "/tracker    -> Tracker")
        print("    " + url + "/map        -> Map Tracker")
        print("    " + url + "/live       -> Live Visibility")
        print("    " + url + "/operations -> Operations")
        print("    " + url + "/health     -> Health Check")
    else:
        print("\n  Could not detect public URL.")
        print("  Check if server is running on port 8000.")

    print("\n  Press Ctrl+C to stop tunnel.")
    
    try:
        proc.wait()
    except KeyboardInterrupt:
        print("\n  Stopping tunnel...")
        proc.terminate()
        print("  Tunnel closed.")

if __name__ == "__main__":
    main()

