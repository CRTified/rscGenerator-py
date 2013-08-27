rscGenerator-py
===============

A small rsCollection generator written in Python.

Please keep the generated rsCollection and the corresponding files in your share.

Usage:
	rscGenerator.py [options] [folder]...

Options:
  -h	--help		Show this screen
  -e	--exclude=REGEX	Excludes files and folders matching the REGEX
			(By matching the name, not the full path)
  -o	--output=FILE	Write the rsCollection into FILE.
			If not given, it will write into ./generated.rscollection
  -s	--stdout	Print the XML-Tree to stdout. It overrides -o, so no file will be created.
  -v	--verbose	Show what the Script is doing
