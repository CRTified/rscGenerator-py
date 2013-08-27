#!/usr/bin/python
import sys
import os
import getopt
import hashlib
import lxml.etree as xml
import re

def hashfile(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()

def isMatching(expressions, target):
    for expression in expressions:
        if re.match(expression, target):
            return True
    return False

def addFolder(parentNode, path, verbose, exclude):
    if verbose:
        print '[READ ] Directory\t' + path
    for entry in os.listdir(path):
        if not isMatching(exclude, entry):
            if os.path.isdir(os.path.join(path, entry)):
                child = xml.Element('Directory', name=entry)
                parentNode.append(child)
                addFolder(child, os.path.join(path, entry), verbose, exclude)
            else:
                addFile(parentNode, path, entry, verbose)

def addFile(parentNode, path, name, verbose): 
    file = os.path.join(path, name)
    if verbose:
        print '[READ ] File\t\t' + file
    child = xml.Element('File')
    child.set('name', name)
    child.set('sha1', hashfile(file))
    child.set('size', str(os.path.getsize(file)))
    parentNode.append(child)

def printHeader():
    print 'rsCollection generator by Amarandus (Do whatever you want with it)'
    print ''
    print 'Please keep the generated rsCollection and the corresponding files in your share.'
    print ''

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

def main():
    if len(sys.argv) <= 1:
        printUsage()
    
    verbose = False
    output  = 'generated.rsCollection'
    exclude = []    
    stdout  = False
    quiet   = False

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

    root = xml.XML('<!DOCTYPE RsCollection><RsCollection />')
    for target in targets:
        addFolder(root, target, verbose, exclude)

    tree = xml.ElementTree(root)

    if stdout:
        print ''
        print xml.tostring(tree, pretty_print=True)
    else:
        if verbose:
            print '[WRITE] File\t\t' + output
        tree.write(output, pretty_print=True)

main()
