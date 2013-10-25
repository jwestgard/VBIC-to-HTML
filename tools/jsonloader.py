import json

vbic = json.load(open('results.json'))

for x in vbic:
    print(x)