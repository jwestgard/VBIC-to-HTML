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

def write_list_to_file(filename, result):
    f = open(filename, 'w')
    f.write('\n'.join(result))
    f.close()

def matchkeys(key, data):
    result = []
    for x in data:
        if key in x['Keywords']:
            result.append(x)
    return result
    
def generate_keylist(keys, data):
    result = []
    for k in keys:
        hits = matchkeys(k, data)
        result.append("<h1>" + k + "</h1>")
        for h in hits:
            result.append("<p><a href='" + h['Link'] + "'>"
                          + h['Title'] + "</a></p>")
    return result

vbic = load_json_dataset('vbic_data5.json')

allkeys = []
allcats = []

for x in vbic:
    for cat in x['Categories']:
        for c in cat:
            if c not in allcats:
                allcats.append(c)
    for key in list(x['Keywords']):
        for k in key:
            if k not in allkeys:
                allkeys.append(k)

print('CATEGORIES:')
allcats.sort()
for c in allcats:
    print(c)

print('KEYWORDS:')
allkeys.sort()
for k in allkeys:
    print(k)

save_json_dataset('vbic_data6.json', vbic)

# catlist = pickle.load(open('categories.p', 'rb'))
# keys = pickle.load(open('keywords.p', 'rb'))
# result = generate_keylist(keys, vbic)