#!/usr/bin/env python
#encoding: utf-8
# author: Sébastien Boisvert
# license: GPLv3

"""
usage:

zcat sequences_16S_all_gg_2011_1_unaligned.fasta.gz | ExtractTree_from_fasta.py  TreeOfLife-Edges_seq.tsv Taxons_seq.tsv

sequences_16S_all_gg_2011_1_unaligned.fasta.gz is from the GreenGenes (paper in ISME 2012)

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

ranks={}
ranks['k__']='kingdom'
ranks['p__']='phylum'
ranks['c__']='class'
ranks['o__']='order'
ranks['f__']='family'
ranks['g__']='genus'
ranks['s__']='species'



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

# >43 AF005049.1 Methanococcus maripaludis str. LL k__Archaea; p__Euryarchaeota; c__Methanococci; o__Methanococcales; f__Methanococcaceae; g__Methanococcus; s__Methanococcus maripaludis; otu_143

#

arcs={}
vertices={}

verticesToNumbers={}

gotHeader=False
debug=False

processed=0
PERIOD=10000

for line in sys.stdin:

	if line[0]!='>':
		continue

	processed+=1

	if processed % PERIOD == 0:
		print "Processed: "+str(processed)

	header=line

	start=header.find("k__")

	tokens=header[start:].split(";")

	path=[]

	for part2 in tokens:
		part=part2.strip()
		if len(part)<3:
			continue

		code=part[0:3]

		if code in ranks:
			key=part.replace(";","")
			path.append(key)

	# add the vertices
	for vertex in path:
		if isDefined(vertex):
			vertices[vertex]=0

	# add the arcs
	i=0
	while i<(len(path)-1):
		parentVertex=path[i]
		childVertex=path[i+1]

		if isDefined(parentVertex) and isDefined(childVertex) and parentVertex!=childVertex:
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
