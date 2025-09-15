import requests
import time

# Wait a few seconds to ensure DB is ready
time.sleep(5)

def test_homepage():
    r = requests.get("http://web:5000/")
    assert r.status_code == 200
    # Check that the HTML contains "Messages" (your h1 in index.html)
    assert "<h1>Messages</h1>" in r.text

def test_db_connection():
    r = requests.get("http://web:5000/db-check")
    assert r.status_code == 200
    assert "DB connection successful!" in r.text
