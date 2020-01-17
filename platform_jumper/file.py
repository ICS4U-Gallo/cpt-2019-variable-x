import json

with open("score.json", "r") as f:
    data = json.load(f)
    
data[''] = 1

with open("score.json", "w") as f:
    json.dump(data, f)

