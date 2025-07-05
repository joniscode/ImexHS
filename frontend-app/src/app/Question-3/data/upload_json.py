import json
import requests

# Cambia la ruta si usas el otro archivo
json_path = "sample-03-json.json"
url = "http://localhost:8000/api/elements/"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

response = requests.post(url, json=data)

print(f"Status Code: {response.status_code}")
print("Response:")
print(response.text)
