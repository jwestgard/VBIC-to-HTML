#!/usr/bin/env python3

def append_item(i):
    result = []
    result.extend(['<h3><a href="', i['Link'],'">'])
    result.extend([i['Title'], '</a>:</h3> '])
    result.extend(['<p>',i['Description']])
    if i['Notes'] != "":
        result.extend(["<br /><strong>NOTE: </strong>", i['Notes']])
    result.append("</p>")
        
    if i['Tags'] != "":
        keyList = i['Tags'].split(',')
        css = []
        css.extend(['font-size: 80%','line-height: 110%'])
        css.extend(['padding: 0px 20px','margin: 0px 25px 20px 25px'])
        css.extend(['border: 0px grey none','border-radius: 5px'])
        css.extend(['background-color: #FAFAFA'])
        result.extend(['<div style="','; '.join(css),'">'])
        result.append('<p style=""><strong>Tags</strong>: ')
        result.append(', '.join(keyList))
        result.append("</p></div>")
    
    return result


def make_list(myData, targetCat):
    resultlist = []
    resultlist.extend(['<html>', '<head></head>', '<body>'])
    resultlist.extend(['<h1>Resources Related to ', targetCat, '</h1>'])
    print(resultlist)
    print(myData)
    print(targetCat)
    
    for i in myData:
        if i['Categories'] != "":
            catList = i['Categories'].split(';')
            print(catList)
            for j in catList:
                print(j)
                if j == targetCat:
                    resultlist.extend(append_item(i))
    
    resultlist.extend(['</body>', '</html>'])
    return resultlist


def main():
    import csv
    cats = ['CAREER','COMPANY','COUNTRY RESEARCH','DEMOGRAPHICS AND STATISTICS']
    cats.extend(['ECONOMICS','ENTREPRENEURSHIP','FINANCE AND INVESTMENT'])
    cats.extend(['INDUSTRY','LOGISTICS, BUSINESS & PUBLIC POLICY'])
    cats.extend(['MARKETING','PRODUCT'])
    print(cats)
    
    sourceFile = input("\nEnter the name of the data file: ")
    cat_req = input("\nEnter the category requested (or type A for all): ")
    with open(sourceFile, 'r') as myFile:
        myData = []
        for row in csv.DictReader(myFile):
            myData.append(row)
            
        if (cat_req == 'A'):
            for c in cats:
                print('\n\n\nChecking for resources related to {0}'.format(c))
                htmlpage = make_list(myData, c)
                print('\n'.join(htmlpage))
                path = 'output/' + c[0:3] + '.html'
                outputFile = open(path, mode='w')
                outputFile.write('\n'.join(htmlpage))
                outputFile.close()
        else:
            print('\n\n\nChecking for resources related to {0}'.format(cat_req))
            htmlpage = make_list(myData, cat_req)
            print('\n'.join(htmlpage))
            path = 'output/' + cat_req[0:3] + '.html'
            outputFile = open(path, mode='w')
            outputFile.write('\n'.join(htmlpage))
            outputFile.close()
main()
