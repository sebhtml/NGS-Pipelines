#!/usr/bin/env python

import xml.dom.minidom
from xml.dom.minidom import Node
 

goldStandard='MetaPhlAn.xml'
mine='ray.xml'

data={}

samples=[]


def addToTree(xmlFile):

	print "Loading "+xmlFile

	doc1 = xml.dom.minidom.parse(xmlFile)
	
	for node in doc1.getElementsByTagName("sample"):
		sampleName=node.getElementsByTagName("name")[0].childNodes[0].nodeValue
	
		if sampleName not in data:
			data[sampleName]={}
		else:
			samples.append(sampleName)

		for entry in node.getElementsByTagName("taxon"):
			rank=entry.getElementsByTagName("rank")[0].childNodes[0].nodeValue
			name=entry.getElementsByTagName("name")[0].childNodes[0].nodeValue
			value=float(entry.getElementsByTagName("value")[0].childNodes[0].nodeValue)
			
			if rank not in data[sampleName]:
				data[sampleName][rank]={}
	
			if name not in data[sampleName][rank]:
				data[sampleName][rank][name]={}
	
			if xmlFile not in data[sampleName][rank][name]:
				data[sampleName][rank][name][xmlFile]=0.0
	
			data[sampleName][rank][name][xmlFile]+=value
		
addToTree(goldStandard)
addToTree(mine)


ranks=["kingdom","phylum","class","order","family","genus","species"]

def showEntries(data,sample,rank,count,stream):

	humanRemove={}
	humanRemove['kingdom']='Metazoa'
	humanRemove["phylum"]='Chordata'
	humanRemove['class']='Mammalia'
	humanRemove['order']='Primates'
	humanRemove['family']='Hominidae'
	humanRemove['genus']='Homo'
	humanRemove['species']='Homo sapiens'

	normalization={}
	normalization['kingdom']=0
	normalization['phylum']=0
	normalization['class']=0
	normalization['order']=0
	normalization['family']=0
	normalization['genus']=0
	normalization['species']=0

	# update values
	for entry in data[sample][rank].items():
		taxon=entry[0]

		if taxon!=humanRemove[rank]:
			continue

		for entry2 in entry[1].items():
			source=entry2[0]
			value=entry2[1]
			
			normalization[rank]=value


	for entry in data[sample][rank].items():
		taxon=entry[0]

		if len(entry[1].items())!=count:
			continue

		stream.write("rank="+rank+"	taxon="+taxon)

		for entry2 in entry[1].items():
			source=entry2[0]
			value=entry2[1]
			
			if source=="ray.xml":
				value=(value/(100.00-normalization[rank]))*100.00

			stream.write("	"+str(value)+"	("+source+")")

			if count==1 and value>=1:
				stream.write("	UNIQUE")

		stream.write("\n")


def generateReport(sample):

	stream=open(sample,"w")

	stream.write("sample= "+sample)
	stream.write("")

	for rank in ranks:
		if rank in data[sample]:

			stream.write("")
			stream.write("\n")
			stream.write("Rank= "+rank)
			stream.write("\n")

			stream.write("")
			stream.write("\n")
			stream.write("In both")
			stream.write("\n")
			stream.write("")
			stream.write("\n")
			showEntries(data,sample,rank,2,stream)
			stream.write("\n")
			
			stream.write("")
			stream.write("\n")
			stream.write("Only in 1")
			stream.write("\n")
			stream.write("")
			stream.write("\n")

			showEntries(data,sample,rank,1,stream)

	stream.close()
				
for sample in samples:
	generateReport(sample)


