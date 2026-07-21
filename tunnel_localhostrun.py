"""
Create a public URL using localhost.run SSH tunnel.
No signup required, free, instant.
"""
import subprocess
import re
import sys
import time
import os

URL_FILE = "public_url.txt"

def main():
    print("=" * 60)
    print("  Creating public URL via localhost.run")
    print("  (No signup required, completely free)")
    print("=" * 60)

    # Ensure old URL file is removed
    if os.path.exists(URL_FILE):
        os.remove(URL_FILE)

    # Use cmd to run ssh and capture output
    cmd = (
        'ssh -o StrictHostKeyChecking=no '
        '-o ServerAliveInterval=30 '
        '-R 80:localhost:8000 '
        'nokey@localhost.run'
    )

    # Use subprocess with shell
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        encoding='utf-8',
        errors='replace'
    )

    url = None
    start_time = time.time()
    timeout = 25

    print("\n  Connecting...")
    print()

    for line in iter(proc.stdout.readline, ""):
        line = line.strip()
        if line:
            # Filter out ANSI escape sequences
            clean = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', line)
            if clean.strip():
                print("  " + clean)
                sys.stdout.flush()

            # Look for URL
            for pattern in [
                r'(https?://[a-zA-Z0-9][-a-zA-Z0-9]*\.localhost\.run)',
                r'([a-zA-Z0-9][-a-zA-Z0-9]*\.localhost\.run)',
            ]:
                m = re.search(pattern, line)
                if m:
                    raw = m.group(1)
                    if not raw.startswith('http'):
                        raw = 'https://' + raw
                    if 'admin' not in raw and 'console' not in raw and raw != 'https://localhost.run':
                        url = raw
                        break
            if url:
                break

        if time.time() - start_time > timeout:
            print("\n  Timeout waiting for URL.")
            break

    if url:
        with open(URL_FILE, 'w') as f:
            f.write(url)

        print()
        print("=" * 60)
        print("  PUBLIC URL: " + url)
        print("=" * 60)
        print()
        print("  Share this URL with anyone: " + url)
        print()
        print("  Available pages:")
        print("    " + url + "             -> Home (Login page)")
        print("    " + url + "/dashboard    -> Dashboard")
        print("    " + url + "/tracker      -> Tracker")
        print("    " + url + "/map          -> Map Tracker")
        print("    " + url + "/live         -> Live Visibility")
        print("    " + url + "/operations   -> Operations")
        print("    " + url + "/health       -> Health Check")
        print("    " + url + "/docs         -> API Docs (Swagger)")
        print()
        print("  Default login:")
        print("    Username: admin")
        print("    Password: admin123")
        print()
        print("  Press Ctrl+C to stop the tunnel.")
    else:
        print()
        print("  Could not detect public URL.")
        print("  Make sure your FastAPI server is running on port 8000.")
        print("  Try: .venv\\Scripts\\uvicorn app.main:app --host 0.0.0.0 --port 8000")

    try:
        proc.wait()
    except KeyboardInterrupt:
        print("\n  Stopping tunnel...")
        proc.terminate()
        print("  Tunnel closed.")

if __name__ == "__main__":
    main()

