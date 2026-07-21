"""
Start an ngrok tunnel to expose the local FastAPI server publicly.
Run this script while the server is running on port 8000.
"""
import sys
import time
from pyngrok import ngrok, conf

# Set the port your FastAPI server is running on
LOCAL_PORT = 8000

def main():
    print("🔌 Starting ngrok tunnel to http://localhost:8000 ...")
    
    # Optional: set your ngrok auth token if you have one (uncomment and add token)
    # ngrok.set_auth_token("YOUR_AUTH_TOKEN")
    
    # Create HTTP tunnel
    http_tunnel = ngrok.connect(LOCAL_PORT, "http")
    
    print("\n✅ ngrok tunnel is live!")
    print(f"\n🌍 Public URL: {http_tunnel.public_url}")
    print(f"\n   Share this URL with anyone to access the app.")
    print(f"\n📋 Available pages:")
    print(f"   {http_tunnel.public_url}           -> Home")
    print(f"   {http_tunnel.public_url}/dashboard  -> Dashboard")
    print(f"   {http_tunnel.public_url}/tracker    -> Tracker")
    print(f"   {http_tunnel.public_url}/map        -> Map Tracker")
    print(f"   {http_tunnel.public_url}/live       -> Live Visibility")
    print(f"   {http_tunnel.public_url}/operations -> Operations")
    print(f"   {http_tunnel.public_url}/health     -> Health Check")
    print(f"   {http_tunnel.public_url}/docs       -> API Docs (Swagger)")
    print(f"\n⚠️  Press Ctrl+C to stop the tunnel and exit.")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping ngrok tunnel...")
        ngrok.kill()
        print("👋 Tunnel closed. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()

