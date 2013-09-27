#!/usr/bin/env python3

import os, csv


# Generates HTML from a line of CSV data
# -- Title w/ hotlink, Description, Keywords

def make_html(i):
    result = ['\n<h3><a href="', i['Link'],'">']
    result.extend([i['Title'],'</a>:</h3>'])
    result.extend(['\n<p>',i['Description']])
    if i['Notes'] != "":
        result.extend(["\n<br /><strong>NOTE: </strong>", i['Notes']])
    result.append("</p>")
        
    if i['Keywords'] != "":
        keyList = i['Keywords'].split(',')
        css = ['font-size: 90%','line-height: 110%']
        css.extend(['padding: 0px 20px','margin: 0px 25px 20px 25px'])
        result.extend(['\n<div style="','; '.join(css),'">'])
        result.append('\n<p><strong>Keywords</strong>: ')
        result.append(', '.join(keyList))
        result.append("</p>\n</div>")
    
    return result


# Creates HTML page for given category, finds matching resources in dataset
# and invokes append_item function for each matching line of data

def make_list(myData, targetCat):
    resultlist = ['<html>\n', '<head></head>\n', '<body>\n']
    resultlist.extend(['<h1>Resources Related to ', targetCat, '</h1>\n'])
    
    for i in myData:
        if i['Categories'] != "":
            catList = i['Categories'].split(';')
            for j in catList:
                if j == targetCat:
                    resultlist.extend(make_html(i))
    
    resultlist.append("\n\n</body>\n</html>")
    return resultlist


# Prompts user to specify name of data file, opens the data file,
# and reads data into a list of dictionaries, which it returns as myData

def read_csv():
    sourceFile = input("\nEnter the name of the data file: ")
    with open(sourceFile, 'r') as myFile:
        myData = []
        for row in csv.DictReader(myFile):
            myData.append(row)
    return myData


# Creates menu of categories that can be searched, gets user selection,
# iterates through dataset finding matches for each category,
# and creates and saves an HTML page for each category

def generate_html(myData):
    cats = ['CAREER','COMPANY','COUNTRY RESEARCH','DEMOGRAPHICS AND STATISTICS']
    cats.extend(['ECONOMICS','ENTREPRENEURSHIP','FINANCE AND INVESTMENT'])
    cats.extend(['INDUSTRY','LOGISTICS, BUSINESS & PUBLIC POLICY'])
    cats.extend(['MARKETING','PRODUCT'])
    
    print('\nType the number to search for one of these categories:')
    for index, item in enumerate(cats):
        print('\t' + str(index) + '\t' + str(item))
    catReq = input("\nOr type A for all: ")
    
    if (catReq == 'A'):
        catList = cats
    else:
        i = int(catReq)
        catList = [cats[i]]
            
    for c in catList:
        print('Checking for resources related to the topic {0}...'.format(c))
        htmlpage = make_list(myData, c)
        path = os.path.join('output', c[0:3] + '.html') 
        outputFile = open(path, mode='w')
        outputFile.write(''.join(htmlpage))
        outputFile.close()
        print('File saved as {0}.'.format(path))


# Asks user to specify data file, and generates text file layed out for
# easy editing
def edit_data(myData):
    spacer = "*" * 35
    result = [spacer, "\n* COMPLETE LIST OF VBIC RESOURCES *\n", spacer]
    
    for i in myData:
        result.extend(["\n\n", "TITLE: ", i['Title']])
        result.extend(["\n\n", "LINK: ", i['Link']])
        result.extend(["\n\n", "DESCRIPTION: ", i['Description']])
        result.extend(["\n\n", "NOTES: ", i['Notes']])
        result.extend(["\n\n", "KEYWORDS (separated by commas): ", i['Tags'].title()])
        
        if (i['Categories']):
            result.extend(["\n\n", "CATEGORIES (w/ rankings): "])
            catsList = i['Categories'].split(";")
            for index, j in enumerate(catsList):
                line = "\n" + str(index + 1) + ") " + j
                result.append(line)
        
        result.extend(["\n\n", spacer])
    
    return result
    
    
def save_file(content):
    filename = input('Enter the name (with extension) under which to save the results: ')
    path = os.path.join('output', filename) 
    outputFile = open(path, mode='w')
    outputFile.write('\n'.join(content))
    outputFile.close()
    print('File saved as {0}.'.format(path))


# asks user to specify keyword list file, and loads the keywords into a list and returns it
def load_keywords():
    sourceFile = input("\nEnter the name of the keyword file: ")
    
    with open(sourceFile) as f:
        keywords = f.read().splitlines()
   
    return keywords


# iterate through keywords from keywords file, for each one, iterate through
# data looking for matches in the keywords field, and if found, call
# the html for that resource and append the html to the result list.
def html_by_keywords(data, keywords):
    result = ['<html>', '<head></head>', '<body>']
    
    for i in keywords:
        print("Searching for resources related to {0}".format(i))
        link = "".join(i.split()).lower()
        result.append("<a id='{0}'><h3>Resources Related to {1}</h3></a>".format(link, i))
        
        for j in data:
            if i in j['Keywords']:
                result.extend(html_kw_item(j))
            else:
                pass
    
    result.extend(['</body>','</html>'])
    return result

    
# create html individual resource listing    
def html_kw_item(resource):
    result = ["<h4><a href='{0}'>{1}</a>:</h4>".format(resource['Link'], resource['Title'])]
    result.extend(["<p>{0}</p>".format(resource['Description'])])
    if resource['Notes'] != "":
        result.extend(["<p><strong>NOTE: {0}</strong></p>".format(resource['Notes'])])
        
    if resource['Keywords'] != "":
        keylist = resource['Keywords'].split(',')
        css = ['font-size: 90%','line-height: 110%']
        css.extend(['padding: 0px 20px','margin: 0px 25px 20px 25px'])
        result.extend(['\n<div style="','; '.join(css),'">'])
        result.append('\n<p><strong>Keywords</strong>: ')
        
        for keyword in keylist:
            link = "".join(keyword.split()).lower()
            item = "<a href='#{0}'>{1}</a>, ".format(link, keyword)
            result.append(item)
            
        result.append("</p>\n</div>")
        
    return result


# The main control for the various functions of this program
def main():
    print("What would you like to do today?")
    task = input("Enter E to create file for editing data, C to generate HTML by categories, or K to generate HTML by keywords: ")
    
    while (task not in ('E','C','K')):
        task = input("You must enter E, C, or K!")
    
    if (task == 'C'):
        myData = read_csv()
        generate_html(myData)
    
    elif (task == 'E'):
        print("You indicated that you want to edit your data!")
        myData = read_csv()
        result = edit_data(myData)
        save_file(result)
        
    if (task == 'K'):
        print("You indicated that you want to create a keyword list!")
        myData = read_csv()
        keywords = load_keywords()
        result = html_by_keywords(myData, keywords)
        save_file(result)
    
    print('\nThanks for using the HTML generator. Goodbye!')
 
main()
