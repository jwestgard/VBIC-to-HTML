import sys
import csv
import json

with open('sample.csv', mode='r') as f:
    reader = csv.DictReader(f)
    out = json.dumps([row for row in reader], indent=4)
    print(out)