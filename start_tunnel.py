"""
Create a public URL for the local FastAPI server using pyngrok.
The server must already be running on port 8000.
"""
import sys
from pyngrok import ngrok, conf

port = 8000
public_url_file = "public_url.txt"

print("=" * 60)
print("  Creating public tunnel to localhost:" + str(port))
print("=" * 60)

try:
    # Kill any existing ngrok tunnels
    ngrok.kill()

    # Start tunnel
    tunnel = ngrok.connect(port, "http")
    public_url = tunnel.public_url

    print("\n  PUBLIC URL: " + public_url)
    print("  (Share this URL with anyone to access the app)")
    print("=" * 60)

    # Save to file
    with open(public_url_file, "w") as f:
        f.write(public_url)

    print("\n  Available pages:")
    print("    " + public_url + "             -> Home (Login Page)")
    print("    " + public_url + "/dashboard    -> Dashboard")
    print("    " + public_url + "/tracker      -> Tracker")
    print("    " + public_url + "/map          -> Map Tracker")
    print("    " + public_url + "/live         -> Live Visibility")
    print("    " + public_url + "/operations   -> Operations")
    print("    " + public_url + "/health       -> Health Check")
    print("    " + public_url + "/docs         -> API Docs (Swagger)")

    print("\n  Dashboard (admin):")
    print("    Username: admin")
    print("    Password: admin123")

    print("\n  Press Ctrl+C to stop the tunnel and exit.")

    # Keep running
    import time
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n  Stopping tunnel...")
    ngrok.kill()
    print("  Tunnel closed.")
except Exception as e:
    print("\n  Error: " + str(e))
    print("\n  Make sure the FastAPI server is running on port 8000.")
    sys.exit(1)

