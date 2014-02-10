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
    result = ["<h2>Frequently Used Sources</h2>"]
    hits = []
    hitcount = 0
    summary = []
    for x in data:
        if category in x['Categories'].keys():
            hitcount += 1
            hits.append(x)
    sorted_hits = sorted(hits, key=lambda c: c['Categories'][category])
    for y in sorted_hits:
        if y['Link']:
            result.append("<p><b><a href='{0}'>{1}</a></b></p>".format(y['Link'], y['Title']))
        else:
            result.append("<p><b>{0}</b></p>".format(y['Title']))
        if y["Notes"]:
            result.append("<div style='font-size: 90%'><p><em>Note: {0}</em></p></div>".format(y["Notes"]))
        result.append("<p>{0}</p>".format(y['Description']))
        summary.append("{0} = {1}".format(y['Title'], str(y['Categories'][category])))
    return result, hitcount, summary

def generate_alphamenu():
    alpha_menu = "<p>"
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for letter in alphabet:
        link = " <a href='#{0}'>{0}</a> |".format(letter)
        if letter == 'A':
            alpha_menu += link[1:]
        elif letter == 'Z':
            alpha_menu += link[:-1]
        else:
            alpha_menu += link
    alpha_menu += "</p>"
    return alpha_menu
 
def generate_resourcelist_by_keyword(allkeys, data):
    result = []
    result.append(generate_alphamenu())
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    summary = ['<h1>All Keywords</h1>']
    for letter in alphabet:
        result.append("<h2 id='{0}'>{0}</h2>".format(letter))
        for key in allkeys:
            if key[0] == letter:
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
        result.append("<div style='font-size: 80%'><p>[<a href='#'>back to top</a>]</p></div>")
    return result, summary

def generate_resourcelist_by_title(data):
    result = []
    result.append(generate_alphamenu())
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for letter in alphabet:
        print('   • Looking for ' + letter + '...')
        heading = "<h3 id='{0}'>{0}</h3>".format(letter)
        result.append(heading)
        result.append("<ul>")
        for x in data:
            if x['Title'][0] in [letter, letter.lower()]:
                item = ''
                if x['Link']:
                    item += "<li><a href='{0}'>{1}</a>".format(x['Link'], x['Title'])
                else:
                    item += "<li>{0}".format(x['Title'])
                if x['Notes']:
                    item += " <div style='font-size: 90%'>[<em>Note: {0}</em>]</div></li>".format(x['Notes'])
                else:
                    item += "</li>"
                result.append(item)
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
            item = "<li><a href='/vbic/topics#{0}'>{1}</a></li>".format(z, y)
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
                items[i] = "<li><a href='/vbic/topics#{0}'>{1}</a></li>".format(link, i)
    result = ["<ul>"]
    sortlist = sorted(items.keys())
    print("\nBuilding Index...")
    for i in sortlist:
        print("   • {0}".format(i))
        result.append(items[i])
    result.append("</ul>")
    return result
    

print("\n" + "*" * 50)
print("\nWelcome to the HTML Generator!")
print("\nLoading data...")
vbic = load_json_dataset('vbic_data_rev12.json')

print("\nGenerating keyword list...")
allkeys = make_master_hitlist(vbic, 'Keywords')
allkeys.sort(key=lambda k: k.lower())

print("Generating categories list...")
allcats = make_master_hitlist(vbic, 'Categories')
allcats.sort()

print("Generating related topics...")
generate_related_topic_lists('rel-topics.json')

print("\nFinding resources by title...")
res_by_title = generate_resourcelist_by_title(vbic)
write_list_to_file('output/res-by-title.html', res_by_title)
print(" => File res-by-title.html written!\n")

print("Finding resources by topic...")
res_by_key, summary_keys = generate_resourcelist_by_keyword(allkeys, vbic)
write_list_to_file('output/res-by-topic.html', res_by_key)
print(" => File res-by-topic.html written!\n")
write_list_to_file('output/summary_topics.html', summary_keys)
print(" => File summary_topics.html written!\n")

summary_cats = ['<h1>List of All Categories</h1>']
for c in allcats:
    result, count, summary = generate_resourcelist_by_category(c, vbic)
    summary_cats.append("<h2>{0}</h2>".format(c))
    summary_cats.append("<ul>")
    for x in summary:
        summary_cats.append("<li>{0}</li>".format(x))
    summary_cats.append("</ul>")
    print("/nFinding resources for " + c + "..." + " found " + str(count))
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
