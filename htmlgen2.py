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
    summary = []
    for x in data:
        if category in x['Categories'].keys():
            hitcount += 1
            hits.append(x)
    sorted_hits = sorted(hits, key=lambda c: c['Categories'][category])
    for y in sorted_hits:
        result.append("\n<p><a href='{0}'>{1}</a></p>".format(y['Link'], y['Title']))
        result.append("<p>{0}</p>".format(y['Description']))
        summary.append("{0} = {1}".format(y['Title'], str(y['Categories'][category])))
    return result, hitcount, summary
    
def generate_resourcelist_by_keyword(allkeys, data):
    result = []
    summary = ['<h1>All Keywords</h1>']
    for key in allkeys:
        hits = matchkeys(key, data)
        link = re.sub(r'\W+', '', key).lower()
        result.append("<h3 id='{0}'>{1}</h3>".format(link, key))
        result.append("<ul>")
        summary.append('<h3>{0}</h3>'.format(key))
        summary.append('<ul>')
        for h in hits:
            if h['Notes']:
                myNote = " [<em>Note: {}</em>]".format(h['Notes'])
            else:
                myNote = ""
            result.append("<li><b><a href='{0}'>{1}</a></b>{2}: {3}</li>".format(h['Link'],
                                                                       h['Title'],
                                                                       myNote,
                                                                       h['Description']))
            summary.append('<li>{0} = {1}</li>'.format(h['Title'], str(h['Keywords'][key])))
        result.append('</ul>')
        summary.append('</ul>')
    return result, summary

def generate_resourcelist_by_title(data):
    result = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for letter in alphabet:
        link = "<a href='#{0}'>{0}</a>&nbsp;".format(letter)
        result.append(link)
    for letter in alphabet:
        print('   • Looking for ' + letter + '...')
        heading = "<h3 id='{0}'>{0}</h3>".format(letter)
        result.append(heading)
        result.append("<ul>")
        for x in data:
            if x['Title'][0] in [letter]:
                result.append("<li><a href='" + x['Link'] + "'>"
                              + x['Title'] + "</a></li>")
        result.append("</ul>")
        result.append("<div style='font-size: 80%'><p>[<a href='#'>back to top</a>]</p></div>")
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

def create_index(allkeys, allcats):
    allitems = allkeys + allcats
    items = {}
    for i in allitems:
        if i not in items.keys():
            if i in allcats:
                link = i.lower()
                items[i] = "<li><a href='/vbic/{0}'>{1}</a></li>".format(link, i)
            else:
                link = re.sub(r'\W+', '', i).lower()
                items[i] = "<li><a href='/vbic/keywords#{0}'>{1}</a></li>".format(link, i)
    print(items)
    result = ["<ul>"]
    sortlist = sorted(items.keys())
    print(sortlist)
    for i in sortlist:
        print(i)
        result.append(items[i])
    result.append("</ul>")
    return result
    

print("\n" + "*" * 50)
print("\nWelcome to the HTML Generator!")
print("\nLoading data...")
vbic = load_json_dataset('vbic_data_rev9.json')

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
res_by_key, summary_keys = generate_resourcelist_by_keyword(allkeys, vbic)
write_list_to_file('output/res-by-keyword.html', res_by_key)
print(" => File res-by-keyword.html written!\n")
write_list_to_file('output/summary_keys.html', summary_keys)
print(" => File summary_keys.html written!\n")

summary_cats = ['<h1>List of All Categories</h1>']
for c in allcats:
    result, count, summary = generate_resourcelist_by_category(c, vbic)
    summary_cats.append("<h2>{0}</h2>".format(c))
    summary_cats.append("<ul>")
    for x in summary:
        summary_cats.append("<li>{0}</li>".format(x))
    summary_cats.append("</ul>")
    print("Finding resources for " + c + "..." + " found " + str(count))
    filename = 'output/' + c[0:3].lower() + '.html'
    write_list_to_file(filename, result)
    print(" => File " + filename + " written!")
    write_list_to_file('output/summary_cats.html', summary_cats)
    print(" => File " + 'summary_cats.html' + " written!")
    
index = create_index(allkeys, allcats)
write_list_to_file('output/index.html', index)
print(" => File " + 'index.html' + " written!")
   
print("\nThank you and goodbye!\n") 
print("*" * 50)

# save_json_dataset('vbic_data7.json', vbic)
# catlist = pickle.load(open('categories.p', 'rb'))
# keys = pickle.load(open('keywords.p', 'rb'))
