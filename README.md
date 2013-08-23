CSV-to-HTML
===========

_NOTES FOR UMD LIB-CODE MEMBERS_: I've added the output directory to the repository, including sample output files.  You may want to delete the output files before attempting to run the program locally, so you can easily see what your local version actually creates. As noted in our meeting, one cross-platform compatibility problem could be the hard-coding of slashes in output file paths (Windows machines would expect \ where UNIX and Mac machines will have /).  I have developed and tested my code exclusively on a Mac.  For the data file, you can use one of the included vbic_data files.  The program assumes that the data will be a CSV file with certain column headers, and that it will be found in the same directory as the python script itself.  It will try to write the output files to a subdirectory called output.

------------------------

These Python scripts were developed for work in Digital Programs and Initiatives at the University of Maryland Libraries. There are three scripts, each of which takes data from a CSV file and converts it to another form:

* htmlgen.py searches for matching keywords in a particular column of the CSV data, and then converts the found data to simple HTML for copying into the Libraries' CMS-based website.  
* htmlgen-alpha.py generates HTML-formatted text from all rows in the CSV for easier proofreading and data cleanup.  
* csv-json.py converts CSV data to JSON, for transfer to other systems.

The included file vbic_data.csv is the primary dataset for which these scripts were developed, and can be used for testing.  By default, htmlgen.py outputs files to the output directory.
