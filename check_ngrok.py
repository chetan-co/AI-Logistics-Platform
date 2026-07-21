"""Check ngrok tunnel status and print the public URL."""
import urllib.request
import json

try:
    r = urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=5)
    data = json.loads(r.read().decode())
    tunnels = data.get("tunnels", [])
    if tunnels:
        print("\n✅ ngrok tunnel is active!")
        for t in tunnels:
            url = t.get("public_url")
            if url:
                print(f"\n🌍 Public URL: {url}")
                print(f"\n   Share this URL with anyone to access the app.")
                print(f"\n📋 Available pages:")
                print(f"   {url}           -> Home")
                print(f"   {url}/dashboard  -> Dashboard")
                print(f"   {url}/tracker    -> Tracker")
                print(f"   {url}/map        -> Map Tracker")
                print(f"   {url}/live       -> Live Visibility")
                print(f"   {url}/operations -> Operations")
                print(f"   {url}/health     -> Health Check")
                print(f"   {url}/docs       -> API Docs (Swagger)")
    else:
        print("No tunnels found.")
except urllib.error.URLError:
    print("ngrok admin interface not available. Make sure ngrok tunnel is running.")
except Exception as e:
    print(f"Error: {e}")

