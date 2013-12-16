#!/usr/bin/python
# Set some defaults:
output    = 'default'           # Default dir to create the *.rscollection ('default' => the current working dir)
exclude   = ['\..+?']           # Default value to exclude files if needed. ('\..+?' => No hidden files (starting with a .)
badChars  = ',&<>*?|\":\'() '   # List of bad characters for filenames. They will be replaced with _
verbose   = False               # Default value for the -v switch
stdout    = False               # Default value for the -s switch
quiet     = False               # Default value for the -q switch
link      = False               # Default value for the -l switch
merge     = False               # Default value for the -m switch
overwrite = False               # Default value for the -w switch

