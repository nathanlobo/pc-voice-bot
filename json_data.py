import json

# code to feed data into json file
data = {
    "bot_name": "Lobo",
}

with open("botData.json", "w") as f:
    json.dump(data, f, indent=4)

# code to get data from json file
with open("botData.json", "r") as f:
    data = json.load(f)

print(data["skills"])  # Output: ['Python', 'Arduino', 'Electronics']

#code to modify data in json file
data["experience"] += 1
data["skills"].append("AI")

with open("botData.json", "w") as f:
    json.dump(data, f, indent=4)
