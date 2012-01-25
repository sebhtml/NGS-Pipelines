#!/usr/bin/python
# 
# Newick format:
#
# example 1
#
# (node_1_1,node_1_2,node_1_3)node_1;
#
# node_1	node_1_1
# node_1	node_1_2
# node_1	node_1_3
#
# example 2
#
# (node_1_1,(node_1_2_1,node_1_2_2)node_1_2,node_1_3)node_1;
#
#
# node_1	node_1_1
# node_1	node_1_2
# node_1	node_1_3
# node_1_2	node_1_2_1
# node_1_2	node_1_2_2

# algorithm:
#
# getEdges(newickString)
#	position of parenthesis 1 := first parenthesis
#	position of parenthesis 2 := matching parenthesis
#	parent := the thing after the parenthesis 2, possibly remove ';'
#
#	children := things separated by ',' (not those within ( ) that are not
#                  parenthesis 1 and 2
#
#    	for child in children
#		getEdges(child.subtree)
#		print edge (child.root, parent)
#

import sys

def getChildren(childString):
	#print childString[0]
	#print childString[len(childString)-1]

	children=[]

	last=0
	position=0

	active=0

	while position<len(childString):
		if childString[position]=='(':
			active+=1
		elif childString[position]==')':
			active-=1
		elif active==0 and childString[position]==',':
			child=childString[last:position]
			children.append(child)

			#print "Child= "+child
			last=position+1

		position+=1

	return children

def getEdges(parent,rootString):

	firstParenthesis=0

	# if there is no parenthesis, we have nothing to do
	if not (rootString.find("(")>=0 and rootString.find(")")>=0):
		return
	
	while firstParenthesis<len(rootString) and rootString[firstParenthesis]!='(':
		firstParenthesis+=1

	active=0
	secondParenthesis=firstParenthesis+1

	while secondParenthesis<len(rootString):
	
		# we found the matching parenthesis
		if rootString[secondParenthesis]==')' and active==0:
			break
		
		if rootString[secondParenthesis]=='(':
			active+=1
		
		if rootString[secondParenthesis]==')':
			active-=1

		secondParenthesis+=1

	root=rootString[secondParenthesis+1:].replace(";","").strip()

	if parent!=-99999:
		print parent+"	"+root
	
	children=getChildren(rootString[(firstParenthesis+1):(secondParenthesis)])

	for child in children:
		getEdges(root,child)

	#print "root= "+root
	#print "first= "+str(firstParenthesis)
	#print "second= "+str(secondParenthesis)

if len(sys.argv) != 2:
	print "usage "
	print sys.argv[0]+" Newick-file"
	sys.exit()

file=sys.argv[1]

rootString=""

for line in open(file):
	rootString+=line.strip()


getEdges(-99999,rootString)
