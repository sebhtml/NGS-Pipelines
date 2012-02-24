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

DUMMY="ed9d97fcce457516ebd75648df295fdf460949d1"
debug=False

def getChildren(childString):
	if debug:
		print "[debug] childString: "+childString
	#print childString[len(childString)-1]

	children=[]

	last=1 # skip the (
	position=0

	active=0

	while position<len(childString):
		if childString[position]=='(':
			active+=1

			if debug:
				print "[debug] got ("

		elif childString[position]==')':

			if debug:
				print "[debug] got )"

			active-=1
			
			if active==0:
				if debug:
					print "[debug] got ) and active=0"

				child=childString[last:position]
				children.append(child)

		elif active==1 and childString[position]==',':
			child=childString[last:position]
			children.append(child)

			if debug:
				print "[debug] got , and active=0"

			#print "Child= "+child
			last=position+1

		position+=1

	if debug:
		print "[debug] children: "+str(children)

	return children

def getEdges(parent,rootString):

	if debug:
		print "[debug] parent= "+parent+" rootString= "+rootString

	firstParenthesis=0

	# if there is no parenthesis, we have nothing to do
	if not (rootString.find("(")>=0 and rootString.find(")")>=0):
		if parent!=DUMMY:
			print parent+"	"+rootString
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

	children=getChildren(rootString[(firstParenthesis+0):(secondParenthesis+1)])

	if parent!=DUMMY:
		print parent+"	"+root

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


getEdges(DUMMY,rootString)
