# Playground file
import json

with open('spot.json', 'r', encoding="utf-16") as f:
    json_text = f.read()
json.loads(json_text)

print(json_text)

