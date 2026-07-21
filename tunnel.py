"""
Start a public SSH tunnel to localhost:8000 using localhost.run
No signup required!
"""
import subprocess
import re
import sys
import os

URL_FILE = "public_url.txt"

def main():
    print("=" * 60)
    print("  Starting tunnel to localhost:8000")
    print("  Using localhost.run (no signup required)")
    print("=" * 60)

    proc = subprocess.Popen(
        ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=30",
         "-R", "80:localhost:8000", "nokey@localhost.run"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    url = None

    for line in iter(proc.stdout.readline, ""):
        line = line.strip()
        if line:
            print(line)
            sys.stdout.flush()

            # Look for various public URL patterns
            for pattern in [
                r"(https?://[a-zA-Z0-9][-a-zA-Z0-9]*\.localhost\.run)",
                r"([a-zA-Z0-9][-a-zA-Z0-9]*\.localhost\.run)",
            ]:
                m = re.search(pattern, line)
                if m:
                    raw = m.group(1)
                    if not raw.startswith("http"):
                        raw = "https://" + raw
                    # Skip admin/localhost.run main domain
                    if "admin" not in raw and raw != "https://localhost.run" and "console" not in raw:
                        url = raw
                        break
            if url:
                break

    if url:
        print("\n" + "=" * 60)
        print("  PUBLIC URL: " + url)
        print("=" * 60)
        with open(URL_FILE, "w") as f:
            f.write(url)
    else:
        print("\n Could not detect public URL.")

    print("\n Share this URL with anyone: " + url)
    print("\n Available pages:")
    print("   " + url + "           -> Home (Login page)")
    print("   " + url + "/dashboard  -> Dashboard")
    print("   " + url + "/tracker    -> Tracker")
    print("   " + url + "/map        -> Map Tracker")
    print("   " + url + "/live       -> Live Visibility")
    print("   " + url + "/operations -> Operations")
    print("   " + url + "/health     -> Health Check")
    print("   " + url + "/docs       -> API Docs (Swagger)")
    print("\n Press Ctrl+C to stop the tunnel.")

    # Keep running
    try:
        proc.wait()
    except KeyboardInterrupt:
        print("\n Stopping tunnel...")
        proc.terminate()
        print(" Tunnel closed.")

if __name__ == "__main__":
    main()

