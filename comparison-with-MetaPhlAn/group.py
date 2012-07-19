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

sample='SRS065335'

ranks=["kingdom","phylum","class","order","family","genus","species"]

def showEntries(data,sample,rank,count):
	for entry in data[sample][rank].items():
		taxon=entry[0]

		if len(entry[1].items())!=count:
			continue

		print taxon,
		for entry2 in entry[1].items():
			source=entry2[0]
			value=entry2[1]
			
			print " "+str(value)+" ("+source+")",

		print ""


def generateReport(sample):

	print "sample= "+sample
	print ""
	for rank in ranks:
		if rank in data[sample]:

			print ""
			print "Rank= "+rank

			print ""
			print "In both"
			print ""
			showEntries(data,sample,rank,2)
			
			print ""
			print "Only in 1"
			print ""
			showEntries(data,sample,rank,1)


				
	

generateReport(sample)


