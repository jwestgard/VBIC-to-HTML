import pickle, json, pprint

def load_json_dataset(filename):
    f = open(filename, 'r')
    result = json.load(f)
    f.close()
    return result

def save_json_dataset(filename, data):
    f = open(filename, 'w')
    f.write(json.dumps(data, sort_keys=True,
                       indent=4, separators=(',', ': ')))
    f.close()

reltopics = load_json_dataset("rel-topics.json")

for x in reltopics.keys():
    print(x)