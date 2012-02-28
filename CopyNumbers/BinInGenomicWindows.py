#!/usr/bin/env python
# encoding: utf-8
# author: Sébastien Boisvert
# license: GPL

"""
Usage:
cat sorted.sam | BinInGenomicWindows windowLength SampleWindowsDirectory

windowLength is the window length (we use 4096)

in the paper above, they use 100 000, but they work on human too.


Based on

High-resolution mapping of copy-number alterations with massively parallel sequencing
Derek Y Chiang, Gad Getz, David B Jaffe, Michael J T O'Kelly, Xiaojun Zhao, Scott L Carter, Carsten Russ, Chad Nusbaum, Matthew Meyerson & Eric S Lander
Nature Methods 6, 99 - 103 (2009) Published online: 30 November 2008
doi:10.1038/nmeth.1276
http://www.nature.com/nmeth/journal/v6/n1/full/nmeth.1276.html#Methods

Section 'Statistical analysis of tumor-normal copy-number ratios'
from the Supplementary information
http://www.nature.com/nmeth/journal/v6/n1/extref/nmeth.1276-S1.pdf

Basically, for a genome of length A, and genomic window length L,
exactly A-L+1 genomic window are computed.


You must provide one sorted sam stream in standard input and a output directory.

Windows are centered.
"""

import os
import sys

profile=False

if profile:
	import profile

if len(sys.argv)!=3:
	print __doc__
	sys.exit(1)

class CreatorOfGenomicWindows:
	def __init__(self,sortedSamStream,genomicWindowLength,outputDirectory):

		print "[CreatorOfGenomicWindows.__init__]: welcome !"

		self.sortedSamStream=sortedSamStream
		self.genomicWindowLength=genomicWindowLength
		self.outputDirectory=outputDirectory

		self.COLUMN_REFERENCE_NAME=3
		self.COLUMN_POSITION=4
		self.FLUSHING_PERIOD=10

		self.referenceLengths={}

		self.currentReferenceName=None
		self.activeWindows={}
		self.currentOutputStream=None
		self.currentOutputStreamReference=None

		self.operations=0
		self.lastPosition=None
		self.debug=False

		os.mkdir(outputDirectory)

	def createThoseFancyGenomicWindows(self):
		for line in self.sortedSamStream:
			tokens=line.split("\t")

			if self.debug:
				print line

			if tokens[0]=="@SQ":
				self.processHeader(tokens)
			else:
				self.processAlignment(tokens)

		self.flushAllActiveWindows()

	def processHeader(self,columns):
		#@SQ     SN:GeneDB|LmjF.36       LN:2682151
		referenceName=columns[1].replace("SN:","").strip()
		referenceLength=int(columns[2].replace('LN:',''))

		self.referenceLengths[referenceName]=referenceLength

	def processAlignment(self,tokens):

		if self.debug:
			print "processAlignment"

		referenceName=tokens[self.COLUMN_REFERENCE_NAME-1]

		if self.currentReferenceName==None:
			self.currentReferenceName=referenceName

		if self.currentReferenceName!=referenceName:

			self.flushAllActiveWindows()

			self.currentReferenceName=referenceName

		position=int(tokens[self.COLUMN_POSITION-1])

		self.lastPosition=position

		self.updateWindows(position,1)

		self.operations+=1

		if len(self.activeWindows) > self.FLUSHING_PERIOD:
			self.flushOldWindows(position)

	# flush old windows
	def flushOldWindows(self,position):

		window=self.getWindowFromPosition(position)

		keys=self.activeWindows.keys()

		flushed=0

		windows={}

		for i in keys:
			if i < window:
				windows[i]=1

		self.flushWindowList(windows)

	def flushWindowList(self,windows):

		flushed=len(windows)

		keys=windows.keys()
		keys.sort()

		for i in keys:
			self.flushActiveWindow(i)

		print "[CreatorOfGenomicWindows.flushWindowList] flushed "+str(flushed)+" windows, position is ",
		print str(self.lastPosition)+" on ref. "+self.currentReferenceName+" with "+str(self.referenceLengths[self.currentReferenceName])
		print "Alignments processed: "+str(self.operations)+" active windows: "+str(len(self.activeWindows))
	
	def getFirstPosition(self,position):
		firstWindow=position-self.genomicWindowLength/2

		if firstWindow<1:
			firstWindow=1

		return firstWindow

	def getLastPosition(self,position):

		referenceLength=self.referenceLengths[self.currentReferenceName]

		space=self.genomicWindowLength/2

		if self.genomicWindowLength%2==0:
			space-=1

		lastWindow=position+space

		if lastWindow>referenceLength:
			lastWindow=referenceLength

		return lastWindow

	def getWindowFromPosition(self,position):
		return position - position % self.genomicWindowLength

	def updateWindows(self,position,count):

		# the position is only in 1 window
		
		window=self.getWindowFromPosition(position)

		if window not in self.activeWindows:
			self.activeWindows[window]=0

		self.activeWindows[window]+=count

		
	def flushAllActiveWindows(self):

		windows={}

		keys=self.activeWindows.keys()

		for i in keys:
			windows[i]=1

		self.flushWindowList(windows)

		self.closeOutputStream()

	def flushActiveWindow(self,window):
		firstPosition=self.getFirstPosition(window)
		lastPosition=self.getLastPosition(window)

		referenceName=self.currentReferenceName

		count=self.activeWindows[window]
		
		if self.currentOutputStreamReference!=referenceName:
			self.closeOutputStream()

		if self.currentOutputStream==None:
			fileName=self.outputDirectory+"/"+self.filterName(referenceName)+".tsv"
			self.currentOutputStream=open(fileName,"w")
			self.currentOutputStreamReference=referenceName

			self.currentOutputStream.write("#GenomicWindow	FirstPosition	LastPosition	Length	Reads\n");

			print "[CreatorOfGenomicWindows.flushActiveWindow] opened "+fileName


		length=lastPosition-firstPosition+1
		self.currentOutputStream.write(str(window)+"	"+str(firstPosition)+"	"+str(lastPosition)+"	"+str(length)+"	"+str(count)+"\n")

		del self.activeWindows[window]

	def filterName(self,name):
		return name.replace("|","_")

	def closeOutputStream(self):
		if self.currentOutputStream!=None:
			self.currentOutputStream.close()
			self.currentOutputStream=None
			self.currentOutputStreamReference=None

genomicWindowLength=int(sys.argv[1])
outputDirectory=sys.argv[2]

sortedSamStream=sys.stdin

theMaker=CreatorOfGenomicWindows(sortedSamStream,genomicWindowLength,outputDirectory)

if profile:
	profile.run("theMaker.createThoseFancyGenomicWindows()")
else:
	theMaker.createThoseFancyGenomicWindows()

