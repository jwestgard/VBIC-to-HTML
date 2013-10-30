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
        if key in x['Keywords'].keys():
            result.append(x)
    return result

def generate_resourcelist_by_category(category, data):
    result = []
    hitcount = 0
    for x in data:
        if category in x['Categories'].keys():
            hitcount += 1
            result.append("\n<p><a href='" + x['Link'] + "'>"
                          + x['Title'] + "</a></p>")
            result.append("<p>" + x['Description'] + "</p>")
    return result, hitcount
    
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
    for x in data:
        for k in x[sourcefield].keys():
            if k not in allhits:
                allhits.append(k)
    return allhits

print("\n" + "*" * 50)
print("\nWelcome to the HTML Generator!")
print("Loading data...")
vbic = load_json_dataset('vbic_data_rev7.json')
print("\nGenerating keyword list...")
allkeys = make_master_hitlist(vbic, 'Keywords')
allkeys.sort()
print("Generating categories list...")
allcats = make_master_hitlist(vbic, 'Categories')
allcats.sort()

print("Finding resources by keyword...")
res_by_key = generate_resourcelist_by_keyword(allkeys, vbic)
write_list_to_file('output/keywords.html', res_by_key)
print("File keywords.html written!\n")

for c in allcats:
    result, count = generate_resourcelist_by_category(c, vbic)
    print("Finding resources for " + c + "..." + " found " + str(count))
    filename = 'output/' + c[0:3] + '.html'
    write_list_to_file(filename, result)
    print("File " + filename + " written!")
   
print("\nThank you and goodbye!\n") 
print("*" * 50)

# save_json_dataset('vbic_data7.json', vbic)
# catlist = pickle.load(open('categories.p', 'rb'))
# keys = pickle.load(open('keywords.p', 'rb'))
