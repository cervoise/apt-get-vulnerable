apt-get-vulnerable
==================

A vulnerability checker for debian system based on dpkg and apt info

Check vulnerables packets from a dpkg -l extract and a apt-get --simulate upgrade extract.
Needs internet access to make the analysis (the tool is downloading official changelog from debian.org).

Usage
==================

Edit vars in apt-get-vulnerable.py for inputs file and debian distrib (squeez, wheezy, jessie).
Run script.
Read HTML output.
