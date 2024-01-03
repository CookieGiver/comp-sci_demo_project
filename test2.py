import requests
import json

request = requests.get(
    "https://www.dictionaryapi.com/api/v3/references/collegiate/json/vooooo", 
    params={"key":"a011b64f-c71e-49f1-8aeb-f1e36e48350f"})

with open("definition.json", "w+") as f:
    json.dump(request.json(), f, indent=4)

x = [1, 2, 3, 4]
y = [2, 3]

for i in list(set(x) - set(y)):
    print(i)