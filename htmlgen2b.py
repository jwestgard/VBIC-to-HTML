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
        for y in x['Keywords']:
            if key in y.keys():
                result.append(x)
    return result
    
def generate_resourcelist_by_keyword(allkeys, data):
    result = []
    for key in allkeys:
        hits = matchkeys(key, data)
        result.append("<h1>" + key + "</h1>")
        for h in hits:
            result.append("<p><a href='" + h['Link'] + "'>"
                          + h['Title'] + "</a></p>")
            result.append("<p>" + h['Description'] + "</p>")
    return result

def make_master_hitlist(data, sourcefield):
    allhits = []
    for resource in data:
        for term in resource[sourcefield]:
            for d in term.keys():
                if d not in allhits:
                    allhits.append(d)
    return allhits

vbic = load_json_dataset('vbic_data6.json')

allkeys = make_master_hitlist(vbic, 'Keywords')
allkeys.sort()
allcats = make_master_hitlist(vbic, 'Categories')
allcats.sort()

res_by_key = generate_resourcelist_by_keyword(allkeys, vbic)
write_list_to_file('keywords.html', res_by_key)

print('CATEGORIES:')
for c in allcats:
    print(c)

print('KEYWORDS:')
for k in allkeys:
    print(k)

# save_json_dataset('vbic_data7.json', vbic)
# catlist = pickle.load(open('categories.p', 'rb'))
# keys = pickle.load(open('keywords.p', 'rb'))
