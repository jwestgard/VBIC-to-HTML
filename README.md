CSV-to-HTML
===========

These Python scripts were developed for work in Digital Programs and Initiatives at the University of Maryland Libraries. There are three scripts, each of which takes data from a CSV file and converts it to another form:

* htmlgen.py searches for matching keywords in a particular column of the CSV data, and then converts the found data to simple HTML for copying into the Libraries' CMS-based website.  
* htmlgen-alpha.py generates HTML-formatted text from all rows in the CSV for easier proofreading and data cleanup.  
* csv-json.py converts CSV data to JSON, for transfer to other systems.

The included file vbic_data.csv is the primary dataset for which these scripts were developed, and can be used for testing.  By default, htmlgen.py outputs files to the output directory.
