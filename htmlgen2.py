import json, re

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
    sorted_result = sorted(result, key=lambda k: k['Keywords'][key]) 
    return sorted_result

def generate_resourcelist_by_category(category, data):
    result = []
    hits = []
    hitcount = 0
    for x in data:
        if category in x['Categories'].keys():
            hitcount += 1
            hits.append(x)
    sorted_hits = sorted(hits, key=lambda k: k['Categories'][category])
    for y in sorted_hits:
        result.append("\n<p><a href='" + y['Link'] + "'>"
                        + y['Title'] + "</a></p>")
        result.append("<p>" + y['Description'] + "</p>")
    return result, hitcount
    
def generate_resourcelist_by_keyword(allkeys, data):
    result = []
    for key in allkeys:
        hits = matchkeys(key, data)
        result.append("<a id='" + key + "'><h3>" + key + "</h3></a>")
        for h in hits:
            result.append("<p><a href='" + h['Link'] + "'>"
                          + h['Title'] + "</a></p>")
            result.append("<p>" + h['Description'] + "</p>")
    return result

def generate_resourcelist_by_title(data):
    result = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return_top = "[<a href='#'>back to top</a>]"
    for letter in alphabet:
        link = "<a href='#{0}'>{0}</a>&nbsp;".format(letter)
        result.append(link)
    for letter in alphabet:
        print('   • Looking for ' + letter + '...')
        heading = "<h3 id='{0}'>{0}</h3> {1}".format(letter, return_top)
        result.append(heading)
        result.append("<ul>")
        for x in data:
            if x['Title'][0] in [letter]:
                result.append("<li><a href='" + x['Link'] + "'>"
                              + x['Title'] + "</a></li>")
        result.append("</ul>")
    return result

def generate_related_topic_lists(sourcefile):
    rel_tops = load_json_dataset(sourcefile)
    for x in rel_tops:
        result = ['<h3>Related Topics</h3>']
        result.append('<ul>')
        for y in rel_tops[x]:
            z = re.sub(r'\W+', '', y).lower()
            item = "<li><a href='/vbic/keywords#{0}'>{1}</a></li>".format(z, y)
            result.append(item)
        result.append("</ul>")
        filename = 'output/rel-' + x[0:3].lower() + '.html'
        write_list_to_file(filename, result)
        print(" => File " + filename + " written!")

def make_master_hitlist(data, sourcefield):
    allhits = []
    for x in data:
        for k in x[sourcefield].keys():
            if k not in allhits:
                allhits.append(k)
    return allhits

print("\n" + "*" * 50)
print("\nWelcome to the HTML Generator!")
print("\nLoading data...")
vbic = load_json_dataset('vbic_data_rev8.json')

print("\nGenerating keyword list...")
allkeys = make_master_hitlist(vbic, 'Keywords')
allkeys.sort()

print("Generating categories list...")
allcats = make_master_hitlist(vbic, 'Categories')
allcats.sort()

print("Generating related topics...")
generate_related_topic_lists('rel-topics.json')

print("\nFinding resources by title...")
res_by_title = generate_resourcelist_by_title(vbic)
write_list_to_file('output/res-by-title.html', res_by_title)
print(" => File res-by-title.html written!\n")

print("Finding resources by keyword...")
res_by_key = generate_resourcelist_by_keyword(allkeys, vbic)
write_list_to_file('output/res-by-keyword.html', res_by_key)
print(" => File res-by-keyword.html written!\n")

for c in allcats:
    result, count = generate_resourcelist_by_category(c, vbic)
    print("Finding resources for " + c + "..." + " found " + str(count))
    filename = 'output/' + c[0:3].lower() + '.html'
    write_list_to_file(filename, result)
    print(" => File " + filename + " written!")
   
print("\nThank you and goodbye!\n") 
print("*" * 50)

# save_json_dataset('vbic_data7.json', vbic)
# catlist = pickle.load(open('categories.p', 'rb'))
# keys = pickle.load(open('keywords.p', 'rb'))
