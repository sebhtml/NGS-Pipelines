#!/usr/bin/python

import sys

if len(sys.argv)!=4:
	print "usage"
	print sys.argv[0]+" entry tree names"
	sys.exit()

entryFile=sys.argv[1]
treeFile=sys.argv[2]
namesFile=sys.argv[3]

mainLine=open(entryFile).read()

tokens=mainLine.split("\t")

identifier=int(tokens[0])

childTable={}
parentTable={}
names={}

for line in open(namesFile):
	tokens=line.split("\t")
	key=int(tokens[0])
	description=tokens[1].strip()
	names[key]=description

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

while current in parentTable:
	path.append(current)
	current=parentTable[current]

i=0

print mainLine

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

	print "/",
	print description+"",

print ""
