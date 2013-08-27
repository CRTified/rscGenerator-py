rscGenerator-py
===============

A small rsCollection generator written in Python.

Please keep the generated rsCollection and the corresponding files in your share.

Usage:
        rscGenerator.py [options] [folder]...

Options:

  -h    --help          Show this screen
  
  -e    --exclude=REGEX Excludes files and folders matching the REGEX
                        (By matching the name, not the full path)
                        
  -o    --output=FILE   Write the rsCollection into FILE.
                        If not given, it will write into ./generated.rscollection
                        
  -s    --stdout        Print the XML-Tree to stdout. It overrides -o, so no file will be created.
  
  -v    --verbose       Show what the Script is doing


License
=========

```
            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2013 Romain Lespinasse <romain.lespinasse@gmail.com>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
