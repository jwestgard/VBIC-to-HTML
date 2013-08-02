#!/usr/bin/env python3

def append_item(i, result):
    result.append('<li><a href="' + i['Link'] + '">' + i['Title'] + '</a></li>')
    return result

def main():
    import csv
    result = ["<!doctype html>","<head>","<title>VBIC</title>","</head>","<body>"]
    sourceFile = input("\nEnter the name of the data file: ")
    myFile = open(sourceFile, 'r').readlines()
    myData = csv.DictReader(myFile)
    
    for i in myData:
        result = append_item(i, result)
        
    result.append("</body>")
    result.append("</html>")
    print('\n'.join(result))
    myFileName = input("\n\nEnter the filename under which to save the results: ")
    outputFile = open(myFileName, mode='w')
    outputFile.write('\n'.join(result))
    outputFile.close()
    
main()
