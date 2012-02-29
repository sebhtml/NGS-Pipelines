#!/usr/bin/env python
#encoding: utf-8
# author: Sébastien Boisvert
# license: GPLv3

"""
usage:

zcat taxonomy_16S_all_gg_2011_1.txt.gz | ExtractTree.py  TreeOfLife-Edges.tsv Taxons.tsv

taxonomy_16S_all_gg_2011_1.txt.gz is from the GreenGenes (paper in ISME 2012)

An improved Greengenes taxonomy with explicit ranks for ecological and evolutionary analyses of bacteria and archaea.
Daniel McDonald, Morgan N Price, Julia Goodrich, Eric P Nawrocki, Todd Z DeSantis, Alexander Probst, Gary L Andersen, Rob Knight and Philip Hugenholtz.
ISME J.
http://www.nature.com/ismej/journal/vaop/ncurrent/full/ismej2011139a.html



TreeOfLife-Edges.tsv Taxons.tsv are compatible with the Ray méta-genome assembler and profiler.


see also http://greengenes.lbl.gov/
see also http://www.secondgenome.com/our-research/2011-greengenes-taxonomy/
see also http://www.nature.com/ismej/journal/vaop/ncurrent/full/ismej2011139a.html

"""

import sys

if len(sys.argv)!=3:
	print __doc__
	sys.exit(1)

def isDefined(vertex):
	return len(vertex) > len("?__")

treeFile=open(sys.argv[1],"w")
taxonFile=open(sys.argv[2],"w")


# a typical line is like (this example lacks a species)
#
# 573145  k__Bacteria; p__Proteobacteria; c__Gammaproteobacteria; o__Enterobacteriales; f__Enterobacteriaceae; g__Escherichia; s__
#
# from this, we gather the arcs, the vertices
#

# full path:

# 146678  k__Bacteria; p__Proteobacteria; c__Gammaproteobacteria; o__Enterobacteriales; f__Enterobacteriaceae; g__Shigella; s__Shigella flexneri

#

arcs={}
vertices={}

verticesToNumbers={}

gotHeader=False
debug=False

processed=0
PERIOD=10000

for line in sys.stdin:
	processed+=1

	if processed % PERIOD == 0:
		print "Processed: "+str(processed)

	if not gotHeader:
		gotHeader=True
		continue
	tokens=line.split("\t")

	sequenceIdentifier=int(tokens[0])

	pathString=tokens[1]

	if debug:
		print line
		print "pathString -> "+pathString

	tokens=pathString.split(";")
	# get the fields
	kingdomVertex=tokens[0].strip()
	phylumVertex=tokens[1].strip()
	classVertex=tokens[2].strip()
	orderVertex=tokens[3].strip()
	familyVertex=tokens[4].strip()
	genusVertex=tokens[5].strip()
	speciesVertex=tokens[6].strip()

	path=[kingdomVertex,phylumVertex,classVertex,orderVertex,familyVertex,genusVertex,speciesVertex]

	# add the vertices
	for vertex in path:
		if isDefined(vertex):
			vertices[vertex]=0

	# add the arcs
	i=0
	while i<(len(path)-1):
		parentVertex=path[i]
		childVertex=path[i+1]

		if isDefined(parentVertex) and isDefined(childVertex):
			if parentVertex not in arcs:
				arcs[parentVertex]={}

			arcs[parentVertex][childVertex]=1

		i+=1

print "Processed: "+str(processed)

# at this point, arcs and vertices are populated.

vertexList=vertices.keys()
vertexList.sort()

# >>> joe="k__King George"
# >>> joe[3:]
# 'King George'
# >>> joe[0:3]
# 'k__'

ranks={}
ranks['k__']='kingdom'
ranks['p__']='phylum'
ranks['c__']='class'
ranks['o__']='order'
ranks['f__']='family'
ranks['g__']='genus'
ranks['s__']='species'

# write vertices
i=0
while i<len(vertexList):
	vertexName=vertexList[i]
	
	taxonNumber=i
	taxonOperationCode=vertexName[0:3]
	taxonName=vertexName[3:]
	taxonRank=ranks[taxonOperationCode]
	
	verticesToNumbers[vertexName]=taxonNumber

	taxonFile.write(str(taxonNumber)+"	"+taxonName+"	"+taxonRank+"\n")
	
	i+=1

taxonFile.close()

# write the arcs in the tree file

parents=arcs.keys()
parents.sort()

for parentVertex in parents:
	childVertices=arcs[parentVertex].keys()
	childVertices.sort()

	parentNumber=verticesToNumbers[parentVertex]

	for childVertex in childVertices:
		childNumber=verticesToNumbers[childVertex]

		treeFile.write(str(parentNumber)+"	"+str(childNumber)+"\n")

treeFile.close()
