import json, pprint, re

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

for x in reltopics:
    result = []
    for y in reltopics[x]:
        stripped = re.sub(r'[\W_]+', '', y)
        anchor = "res-by-keyword.html#" + stripped
        result.append("<a href='{0}'>{1}</a><br />".format(anchor, y))
    print(result)
    filename = "output/rel-kw-" + x[0:3].lower() + ".html"
    f = open(filename, 'w')
    f.write('\n'.join(result))
    f.close()
    