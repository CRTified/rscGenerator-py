#!/usr/bin/python
# 
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2013 Richard Schneider
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#     TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#     
#    0. You just DO WHAT THE FUCK YOU WANT TO.
#

# imports
import string
import sys
import os
import getopt
import hashlib
import lxml.etree as xml
import re
import settings

# function to calculate the sha1 of a file
def hashfile(filepath):
    verboseprint('CALC', 'Hash of ' + filepath)
    sha1 = hashlib.sha1()
    f = open(filepath, 'r')
    try:    
        for chunk in iter(lambda: f.read(160), b''): # Read blockwise to avoid python's MemoryError
            sha1.update(chunk)
    finally:
        f.close()
    return sha1.hexdigest()

# function to check whether the list of expressions creates a match
def isMatching(expressions, target):
    for expression in expressions:
        if re.match(expression, target):
            return True
    return False

#####################################################################################
## Link generation
#####################################################################################

# Function to start the scan for generating the links
def link_startScan(target):
    if os.path.isdir(target):
        link_addFolder(target)
    else:
        link_addFile(target)

# recursive function to walk the folder and print the files' links
def link_addFolder(path):
    for entry in os.listdir(path):
        if not isMatching(settings.exclude, entry): # Check for a match with one of the exclude-regEx
            entrypath = os.path.join(path, entry) # Build the entry's path

            if os.path.isdir(entrypath):
                link_addFolder(entrypath) # recursive call
            else:
                link_addFile(entrypath) # Print the file's link

# function to print a file's link
def link_addFile(file):

    path, name = os.path.split(file)
    sha1 = hashfile(file)
    size = str(os.path.getsize(file))

    print 'retroshare://file?name=' + name + '&size=' + size + '&hash=' + sha1


#####################################################################################
## XML generation
#####################################################################################

# Function to start the scan for a XML-Tree
def xml_startScan(parentNode, target):
    verboseprint('SCAN', 'Initialize scan on ' + target)

    if os.path.isdir(target):
        xml_addFolder(parentNode, target)
    else:
        foldername = unicode(os.path.basename(os.path.normpath(os.path.dirname(target))), encoding='utf-8')
        foldernode = xml.Element('Directory', name=foldername)
        parentNode.append(foldernode)

        xml_addFile(foldernode, target)

# recursive function to walk the folder and add the content to the xml-tree
def xml_addFolder(parentNode, path):
    foldername = unicode(cleanFilename(os.path.basename(os.path.normpath(path))), encoding='utf-8')

    verboseprint('READ', 'Directory\t' + foldername)

    foldernode = xml.Element('Directory', name=foldername)
    parentNode.append(foldernode)

    for entry in os.listdir(path):
        if not isMatching(settings.exclude, entry): # Check for a match with one of the exclude-regEx
            entrypath = os.path.join(path, entry)

            if os.path.isdir(entrypath):
                xml_addFolder(foldernode, entrypath) # recursive call
            else:
                xml_addFile(foldernode, entrypath) # Add file

# function to add a file to the tree
def xml_addFile(parentNode, file):
    verboseprint('READ', 'File\t' + file)

    path, name = os.path.split(file)
    sha1 = hashfile(file)
    size = str(os.path.getsize(file))
    childNode = xml.Element('File')
    childNode.set('name', unicode(cleanFilename(name), encoding='utf-8'))
    childNode.set('sha1', sha1)
    childNode.set('size', size)
    parentNode.append(childNode)

# function to write the xml to stdout
def xml_writeToStdout(root):
    tree = xml.ElementTree(root)
    print xml.tostring(tree, pretty_print=True)

# function to write the xml to a file
def xml_writeToFile(root, file):
    verboseprint('SAVE', 'File ' + settings.output)
    tree = xml.ElementTree(root)
    tree.write(file, pretty_print=True)

# function to generate the path where to save the file (can prevent overwriting)
def getSaveFile(base):
    if not settings.overwrite and os.path.exists(base + '.rscollection'):
        verboseprint('SAVE', 'Would overwrite ' + base + '.rscollection')
        writeNumber = 1
        while os.path.exists(base + '-' + str(writeNumber) + '.rscollection'):
            verboseprint('SAVE', 'Would overwrite ' + base + '-' + str(writeNumber) + '.rscollection')
            writeNumber += 1
        base = base + '-' + str(writeNumber)
    return base + '.rscollection'

# function to handle the save-process
def save(root, target):
    if settings.stdout: # if it should write to stdout
        xml_writeToStdout(root)
    else: # if it should write to a file

        if settings.output is 'default':
            settings.output_t = getSaveFile(os.path.basename(os.path.normpath(target)))
        else:
            settings.output_t = getSaveFile(os.path.join(settings.output, os.path.basename(os.path.normpath(target))))

        xml_writeToFile(root, settings.output_t)
        print ''
        link_addFile(settings.output_t)
        print ''



#####################################################################################
## Print Strings
#####################################################################################

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
    print 'Usage:'
    print '\trscGenerator.py [options] [folder]...'
    print ''
    print 'Options:'
    print '  -e\t--exclude=REGEX\tExcludes files and folders matching the REGEX'
    print '\t\t\t(By matching the name, not the full path).'
    print '  -h\t--help\t\tShow this screen.'
    print '  -l\t--link\t\tPrints retroshare://-links to copy and paste.'
    print '  -m\t--merge\t\tMerges all targets to one rsCollection.'
    print '  -o\t--output=FILE\tWrite the rsCollection into FILE and prints a retroshare://-link of the collection.'
    print '\t\t\tIf not given, it will write into <Name of folder>.rscollection.' 
    print '  -q\t--quiet\t\tPrevents any output except -s, -l or the link to a new rsCollection file.'
    print '  -s\t--stdout\tPrint the XML-Tree to stdout. It overrides -o, so no file will be created.'
    print '\t\t\tIt also prevents any output except the XML-Tree.'
    print '  -v\t--verbose\tShow what the Script is doing.'
    print '  -w\t--overwrite\tOverwrites rsCollections if the file already exists.'



#####################################################################################
## Background support
#####################################################################################

def cleanFilename(filename):
    badChars = ' ,&<>*?|\":\'()'
    mapTo    = ''
    for i in range(0, len(badChars)):
        mapTo += '_'
    return filename.translate(string.maketrans(badChars, mapTo))

def parseArguments():
    argletters = 'hve:o:slqmw'
    argwords     = ['help', 'exclude=', 'output=', 'verbose', 'stdout', 'link', 'quiet', 'merge', 'overwrite']
    triggers, targets = getopt.getopt(sys.argv[1:], argletters, argwords) 
    
    if len(targets) is 0:
        printHeader()
        printUsage()
        exit()

    for trigger, value in triggers:
        if trigger in ['-h', '--help']:
            printHeader()
            printUsage()
            exit()
        elif trigger in ['-e', '--exclude']:
            settings.exclude.append(value)
        elif trigger in ['-o', '--output']:
            settings.output = value
        elif trigger in ['-v', '--verbose']:
            settings.verbose = True
        elif trigger in ['-s', '--stdout']:
            settings.stdout = True
            settings.quiet  = True
        elif trigger in ['-l', '--link']:
            settings.quiet = True
            settings.link  = True
        elif trigger in ['-q', '--quiet']:
            settings.quiet = True
        elif trigger in ['-m', '--merge']:
            settings.merge = True
        elif trigger in ['-w', '--overwrite']:
            settings.overwrite = True
    return targets

# Verbose-helper
def verboseprint(tag, string):
    if settings.verbose and not settings.quiet:
        print '[' + tag + ']\t' + string

#####################################################################################
## Main
#####################################################################################

def main():
    # Care for the arguments
    targets = parseArguments()
    
    if not settings.quiet:
        printHeader()

    if settings.merge:
        root = xml.XML('<!DOCTYPE RsCollection><RsCollection />')

    for target in targets:
        if not settings.merge:
            root = xml.XML('<!DOCTYPE RsCollection><RsCollection />')

        if settings.link:
            link_startScan(target)
        else:
            xml_startScan(root, target)

            if not settings.merge:
                save(root, target)

    if settings.merge:
        save(root, target) # Maybe a bit dirty, because target is only inside of the loop.

main()
