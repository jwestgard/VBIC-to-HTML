## Pseudocode for htmlgen.py

1. import csv module (for interpreting data file)
2. prompt the user to specify the data file
3. prompt the user to choose a topic (or choose all)
4. if the response is 'A', set the list of catalogs to be checked to all
5. otherwise, set the catalog to be checked to the chosen number
6. create an empty list to hold data
7. for each row in the datafile, append the row as an dict (set of key => value pairs) to the data list
8. 