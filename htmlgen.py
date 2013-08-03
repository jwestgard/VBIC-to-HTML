#!/usr/bin/env python3

def append_item(i):
    result = ['<h3><a href="', i['Link'],'">']
    result.extend([i['Title'], '</a>:</h3> '])
    result.extend(['<p>',i['Description']])
    if i['Notes'] != "":
        result.extend(["<br /><strong>NOTE: </strong>", i['Notes']])
    result.append("</p>")
        
    if i['Tags'] != "":
        keyList = i['Tags'].split(',')
        css = ['font-size: 80%','line-height: 110%']
        css.extend(['padding: 0px 20px','margin: 0px 25px 20px 25px'])
        css.extend(['border: 0px grey none','border-radius: 5px'])
        css.extend(['background-color: #FAFAFA'])
        result.extend(['<div style="','; '.join(css),'">'])
        result.append('<p><strong>Tags</strong>: ')
        result.append(', '.join(keyList))
        result.append("</p></div>")
    
    return result


def make_list(myData, targetCat):
    resultlist = ['<html>', '<head></head>', '<body>']
    resultlist.extend(['<h1>Resources Related to ', targetCat, '</h1>'])
    
    for i in myData:
        if i['Categories'] != "":
            catList = i['Categories'].split(';')
            for j in catList:
                if j == targetCat:
                    resultlist.extend(append_item(i))
    
    resultlist.extend(['</body>', '</html>'])
    return resultlist


def main():
    import csv
    
    sourceFile = input("\nEnter the name of the data file: ")
    
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
        
    with open(sourceFile, 'r') as myFile:
        myData = []
        
        for row in csv.DictReader(myFile):
            myData.append(row)
            
        for c in catList:
            print('Checking for resources related to the topic {0}...'.format(c))
            htmlpage = make_list(myData, c)
            path = 'output/' + c[0:3] + '.html'
            outputFile = open(path, mode='w')
            outputFile.write('\n'.join(htmlpage))
            outputFile.close()
            print('File saved as {0}.'.format(path))
    
    print('\nThanks for using the HTML generator. Goodbye!')
 
main()
