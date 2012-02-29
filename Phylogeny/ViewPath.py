#!/usr/bin/python
#encoding: utf-8
# author: Sébastien Boisvert
# license: GPLv3

"""
usage
ViewPath.py taxonIdentifier treeFile taxonFile



treeFile contains the taxonomic tree, one edge per line

taxonFile contains the taxons, each line must have:

taxon identifier	taxon name
"""

import sys

if len(sys.argv)!=4:
	print __doc__
	sys.exit()

treeFile=sys.argv[2]
namesFile=sys.argv[3]

identifier=int(sys.argv[1])

childTable={}
parentTable={}
names={}
ranks={}

for line in open(namesFile):
	tokens=line.split("\t")
	key=int(tokens[0])
	description=tokens[1].strip()
	rank=tokens[2].strip()
	names[key]=description
	ranks[key]=rank

for line in open(treeFile):
	tokens=line.split("\t")
	parent=int(tokens[0])
	child=int(tokens[1])

	if parent not in childTable:
		childTable[parent]=[]

	childTable[parent].append(child)

	parentTable[child]=parent

print "parentTable "+str(len(parentTable))
print "childTable "+str(len(childTable))

path=[]

current=identifier

path.append(current)

while current in parentTable:
	current=parentTable[current]
	path.append(current)

i=0

print "identifier: "+str(identifier)
print "path length: "+str(len(path))


i=len(path)-1

newPath=[]

while i>=0:
	newPath.append(path[i])
	i-=1

path=newPath

for i in path:
	description="Unknown (id="+str(i)+")"

	if i in names:
		description=names[i]

	print "-"
	print " rank= "+ranks[i]
	print " taxon= "+description
	print " id= "+str(i)

print ""
