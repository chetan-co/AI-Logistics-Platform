$ErrorActionPreference = 'Stop'
$env:DATABASE_URL = 'postgres://postgres:postgres@localhost:5432/logistics'
$env:AUTH_REQUIRED = 'true'
$env:JWT_SECRET = 'local-dev-secret'
Set-Location 'c:/Users/Bharat Yadav/OneDrive/Desktop/Logistics'
& 'c:/Users/Bharat Yadav/OneDrive/Desktop/Logistics/.venv/Scripts/python.exe' -m uvicorn app.main:app --host 127.0.0.1 --port 8010
