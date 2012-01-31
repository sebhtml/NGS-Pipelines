#!/usr/bin/env python
# encoding= utf-8
# author: Sébastien Boisvert
# 2012-01-31

# this program converts the input stream to coverage files
# specification: http://samtools.sourceforge.net/SAM1.pdf

# this class process a sam file
# to produce coverage depth
class SamProcessor:
	# constructor
	def __init__(self):
		self.column_RNAME=3
		self.column_POS=4
		self.column_SEQ=10
		self.UNMAPPED="*"

		self.lastFlushedPosition=None
		self.lastPosition=None
		self.cacheStore={}
		self.currentReference=None
		self.file=None
		self.processedEntries=0
		self.unmapped=False
		self.matches=0
		self.summary=open("Summary.tsv","w")
		self.summary.write("Reference\tLength in nucleotides\tPositions with reads\tRatio\tMode read depth\n")

		self.referenceLengths={}
		self.frequencies={}
	
	# a line:
	# DD63XKN1:189:C08FBACXX:5:1101:18149:4470        16      gi|115304210|ref|NC_008363.1|:254-778   1       0       30M     *       0       0       ATGCAAACACAAAACGGTGGCAGACCCACA  IJIJJJIJIJIGGHJJJGHGGHFFFFFCCC  AS:i:30 XS:i:0  XF:i:3  XE:i:1  NM:i:0
	def updateReferencePositionCacheEntries(self,line):

		tokens=line.split("\t")

		#@SQ     SN:ref|NC_002662.1|:358-1725    LN:1368
		if tokens[0]=="@SQ":
			reference=tokens[1].replace("SN:","").strip()
			referenceLength=int(tokens[2].replace("LN:","").strip())
			self.referenceLengths[reference]=referenceLength

		if len(tokens)<8:
			self.processedEntries+=1
			return

		reference=tokens[self.column_RNAME-1].strip()

		if reference==self.UNMAPPED:
			self.processedEntries+=1
			self.unmapped=True
			return

		position=int(tokens[self.column_POS-1].strip())
		sequenceLength=len(tokens[self.column_SEQ-1].strip())

		# this is the first entry
		# or this is the beginning of another reference
		if self.currentReference==None or self.currentReference!=reference:

			self.flushAllCacheEntries()
			self.currentReference=reference
			fileName=self.removeFancySymbols(self.currentReference)+".CoverageDepth.tsv"

			self.lastFlushedPosition=None
			self.lastPosition=None
			self.file=open(fileName,"w")
			self.frequencies={}
			self.matches=0

		# update cached entries
		i=0
		while i<sequenceLength:
			cachedPosition=position+i

			if cachedPosition not in self.cacheStore:
				self.cacheStore[cachedPosition]=0

			self.cacheStore[cachedPosition]+=1
			i+=1

		self.lastPosition=position
		self.processedEntries+=1

	# flush cache entries with 0 future references
	def flushNotReferencedCacheEntries(self):
		if self.lastPosition==None:
			return

		keys=self.cacheStore.keys()

		for cachedPosition in keys:
			if cachedPosition < self.lastPosition:
				self.flushCacheEntry(cachedPosition)

	def flushAllCacheEntries(self):
		print "flushing all cache entries"

		keys=self.cacheStore.keys()

		for cachedPosition in keys:
			self.flushCacheEntry(cachedPosition)

		if self.file!=None:
			# before closing, flush all empty positions
			# from lastFlushedPosition+1 to referenceLength

			self.flushEmptyEntries(self.lastFlushedPosition+1,self.referenceLengths[self.currentReference])
			self.file.close()
			self.file=None

			fileName=self.removeFancySymbols(self.currentReference)+".CoverageDepthFrequencies.tsv"

			f=open(fileName,"w")

			keys=self.frequencies.keys()
			keys.sort()
	
			mode=None
			best=None
			for i in keys:
				count=self.frequencies[i]
				f.write(str(i)+"\t"+str(count)+"\n")

				if mode==None or count > best:
					mode=i
					best=count

			theLength=self.referenceLengths[self.currentReference]
			ratio=(0.0+self.matches)
			if theLength!=0:
				ratio/=theLength

			self.summary.write(self.removeFancySymbols(self.currentReference)+"\t"+str(theLength)+"\t"+str(self.matches)+"\t"+str(ratio)+"\t"+str(mode)+"\n")

	def flushCacheEntry(self,cachedPosition):
		if cachedPosition> self.referenceLengths[self.currentReference]:
			self.deleteCacheEntry(cachedPosition)
			return

		# before flushing the entry
		# we want to flush everything with 0 before cachedPosition

		if self.lastFlushedPosition==None:
			self.flushEmptyEntries(1,cachedPosition-1)

		# flush from lastFlushedPosition+1 to cachedPosition-1
		self.flushEmptyEntries(self.lastFlushedPosition+1,cachedPosition-1)

		depth=self.cacheStore[cachedPosition]
		self.writeEntry(cachedPosition,depth)

		if depth not in self.frequencies:
			self.frequencies[depth]=0
		self.frequencies[depth]+=1

		self.lastFlushedPosition=cachedPosition
	
		self.deleteCacheEntry(cachedPosition)

		self.matches+=1

	def writeEntry(self,position,depth):
		self.file.write(str(position)+"\t"+str(depth)+"\n")

	def deleteCacheEntry(self,cachedPosition):
		del(self.cacheStore[cachedPosition])

	def getProcessedEntries(self):
		return self.processedEntries

	def getUnmapped(self):
		return self.unmapped

	def flushEmptyEntries(self,startPosition,endPosition):

		i=startPosition
		while i<=endPosition:
			self.writeEntry(i,0)
			i+=1

		self.lastFlushedPosition=endPosition
	
	def removeFancySymbols(self,text):
		return text.replace(" ","_").replace("/","_").replace("|","_").replace(":","_")

	def writeSummary(self):
		self.summary.close()
		self.summary=None
import sys

CONFIG_CACHE_FLUSH_PERIOD= 4096

virtualProcessor=SamProcessor()

for line in sys.stdin:
	virtualProcessor.updateReferencePositionCacheEntries(line)

	if virtualProcessor.getProcessedEntries()%CONFIG_CACHE_FLUSH_PERIOD==0:
		print "processed "+str(virtualProcessor.getProcessedEntries())+" entries"
		virtualProcessor.flushNotReferencedCacheEntries()

	# the unmapped stuff has begun
	if virtualProcessor.getUnmapped():
		print "First unmapped entry, stopping!"
		break

virtualProcessor.flushAllCacheEntries()

virtualProcessor.writeSummary()

print "job finished !"

