import requests
import time

URL = "http://127.0.0.1:8000/submit"
payload = {
    "problem": "test wifi",
    "university": "test uni",
    "location": "library",
    "solution": "turn it off and on",
    "author": "tester"
}

print("Firing 5 rapid requests to /submit (Limit is 3 per minute)...")

for i in range(1, 11):
    response = requests.post(URL, json=payload)
    print(f"Request {i}: Status Code {response.status_code} -> {response.text}")