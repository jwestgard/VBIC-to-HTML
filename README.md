VBIC-to-HTML
===========

These Python scripts were developed for work in Digital Programs and Initiatives at the University of Maryland Libraries. The basic task was to convert a semi-relational set of data into HTML pages that could be easily imported into the Libraries CMS-based website.

Though the script was developed for a particular dataset, the Virtual Business Information Center, the basic structure and logic of the script could fairly easily be adapted for use with other data.

Running the script with the following command

`python3 htmlgen2.py`
  
will produce a series of html files stored in output/ representing data pulled from the files vbic-data-revXX.json and rel-topics.json, and arranged in various permutations according to the logic of the VBIC website.  These files include a list of resources organized alphbetically (res-by-title.html), one organized by certain topic keywords (res-by-topic.html), and series of resource lists (com.html, etc.) and clickable related-topic links (rel-com.html, etc.), as well as few miscellaneous report files.
