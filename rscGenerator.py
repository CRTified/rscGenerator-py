#!/usr/bin/python
# 
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2013 Romain Lespinasse <romain.lespinasse@gmail.com>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#   
#  0. You just DO WHAT THE FUCK YOU WANT TO.
#

# imports
import sys
import os
import getopt
import hashlib
import lxml.etree as xml
import re

# function to calculate the sha1 of a file
def hashfile(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()

# function to check whether the list of expressions creates a match
def isMatching(expressions, target):
    for expression in expressions:
        if re.match(expression, target):
            return True
    return False

# recursive function to walk the folder and add the content to the xml-tree
def addFolder(parentNode, path, verbose, exclude):
    if verbose:
        print '[READ ] Directory\t' + path
    for entry in os.listdir(path):
        if not isMatching(exclude, entry): # Check for a match with one of the exclude-regEx
            if os.path.isdir(os.path.join(path, entry)):
                child = xml.Element('Directory', name=entry)
                parentNode.append(child)
                addFolder(child, os.path.join(path, entry), verbose, exclude) # recursive call
            else:
                addFile(parentNode, path, entry, verbose) # Add file

# function to add a file to the tree
def addFile(parentNode, path, name, verbose): 
    file = os.path.join(path, name)
    if verbose:
        print '[READ ] File\t\t' + file
    child = xml.Element('File')
    child.set('name', name)
    child.set('sha1', hashfile(file))
    child.set('size', str(os.path.getsize(file)))
    parentNode.append(child)

# function to print the header with basic informations about this script
def printHeader():
    print 'rsCollection generator by Amarandus'
    print ''
    print 'This script is released under the'
    print 'DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE Version 2'
    print '(Check the Code for the full license)'
    print ''
    print 'Please be social and keep the generated rsCollection and the corresponding files in your share.'
    print ''

# function to print the usage and exit
def printUsage():
    printHeader()
    print 'Usage:'
    print '\trscGenerator.py [options] [folder]...'
    print ''
    print 'Options:'
    print '  -h\t--help\t\tShow this screen'
    print '  -e\t--exclude=REGEX\tExcludes files and folders matching the REGEX'
    print '\t\t\t(By matching the name, not the full path)'
    print '  -o\t--output=FILE\tWrite the rsCollection into FILE.'
    print '\t\t\tIf not given, it will write into ./generated.rscollection' 
    print '  -s\t--stdout\tPrint the XML-Tree to stdout. It overrides -o, so no file will be created.'
    print '\t\t\tIt also prevents any output except the XML-Tree.'
    print '  -v\t--verbose\tShow what the Script is doing'
    exit()

# main-function
def main():
    if len(sys.argv) <= 1: # Not enough arguments
        printUsage()
    
    # Set some defaults:
    verbose = False
    output  = 'generated.rsCollection'
    exclude = []    
    stdout  = False
    quiet   = False
    
    # Care for the arguments
    argletters = 'hve:o:sq'
    argwords   = ['help', 'exclude=', 'output=', 'verbose', 'stdout', 'quiet']
    triggers, targets = getopt.getopt(sys.argv[1:], argletters, argwords) 
    if len(targets) is 0:
        printUsage()
    
    for trigger, value in triggers:
        if trigger in ['-h', '--help']:
            printUsage()
        elif trigger in ['-e', '--exclude']:
            exclude.append(value)
        elif trigger in ['-o', '--output']:
            output = value
        elif trigger in ['-v', '--verbose']:
            verbose = True
        elif trigger in ['-s', '--stdout']:
            stdout = True
            quiet  = True
            
    if quiet:
        verbose = False
    
    if not quiet:
        printHeader()
    
    # Create XML-tree
    root = xml.XML('<!DOCTYPE RsCollection><RsCollection />')
    for target in targets:
        addFolder(root, target, verbose, exclude)
    
    # Make it an ElementTree
    tree = xml.ElementTree(root)
    
    # Print it or write it to a file
    if stdout:
        print ''
        print xml.tostring(tree, pretty_print=True)
    else:
        if verbose:
            print '[WRITE] File\t\t' + output
        tree.write(output, pretty_print=True)

#call the main function
main()
