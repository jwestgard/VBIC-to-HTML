#!/usr/bin/env python3

import os, csv


# Generates HTML from a line of CSV data
# -- Title w/ hotlink, Description, Keywords
def append_item(i):
    result = ['\n<h3><a href="', i['Link'],'">']
    result.extend([i['Title'],'</a>:</h3>'])
    result.extend(['\n<p>',i['Description']])
    if i['Notes'] != "":
        result.extend(["\n<br /><strong>NOTE: </strong>", i['Notes']])
    result.append("</p>")
        
    if i['Tags'] != "":
        keyList = i['Tags'].split(',')
        css = ['font-size: 90%','line-height: 110%']
        css.extend(['padding: 0px 20px','margin: 0px 25px 20px 25px'])
        result.extend(['\n<div style="','; '.join(css),'">'])
        result.append('\n<p><strong>Keywords</strong>: ')
        result.append(', '.join(keyList))
        result.append("</p>\n</div>")
    
    return result


# Creates HTML page for given keyword, finds matching resources in dataset
# and invokes append_item function for each matching line of data
def make_list(myData, targetCat):
    resultlist = ['<html>\n', '<head></head>\n', '<body>\n']
    resultlist.extend(['<h1>Resources Related to ', targetCat, '</h1>\n'])
    
    for i in myData:
        if i['Categories'] != "":
            catList = i['Categories'].split(';')
            for j in catList:
                if j == targetCat:
                    resultlist.extend(append_item(i))
    
    resultlist.append("\n\n</body>\n</html>")
    return resultlist


# Prompts user to specify name of data file, opens the data file,
# and reads data into a list of dictionaries, which is returns as myData
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
        
    path = os.path.join('output', 'edit_data' + '.txt') 
    outputFile = open(path, mode='w')
    outputFile.write(''.join(result))
    outputFile.close()
    print('File saved as {0}.'.format(path))



def main():
    
    print("What would you like to do today?")
    task = input("Enter E to edit data, G to generate HTML: ")
    
    while (task not in ('E','G')):
        task = input("You must enter either E or G!")
    
    if (task == 'G'):
        myData = read_csv()
        generate_html(myData)
    
    elif (task == 'E'):
        print("You indicated that you want to edit your data!")
        myData = read_csv()
        edit_data(myData)
    
    print('\nThanks for using the HTML generator. Goodbye!')
 
main()
