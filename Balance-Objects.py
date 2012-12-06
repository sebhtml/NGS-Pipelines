#!/usr/bin/env python
# encoding: UTF-8
# This is a solver for a simple binning problem
# It just do random swap and minimize an objective function
# Author: Sébastien Boisvert
# License: GPLv3

import sys
import random

arguments=sys.argv

if len(arguments)!=3:
	print("Usage: "+arguments[0]+" Entries Bins")
	print("Entries is a 2-column file, the columns are: object description, oject weight")
	print("This program outputs an optimal layout of objects in bins so that all the bins have equal weight or so")
	sys.exit()

inputFile=arguments[1]
bins=int(arguments[2])

objects=[]
binWeights=[]

indexName=0
indexWeight=1
indexBin=2

i=0
while i<bins:
	binWeights.append(0)
	i+=1

print("Configuring for "+str(bins)+" bins")

print("Reading "+inputFile)

stream=open(inputFile)

selectedBin=0
for line in stream:
	
	tokens=line.split()
	weight=int(tokens[1])
	objects.append([tokens[0],weight,selectedBin])
	binWeights[selectedBin]+=weight

stream.close()

print("Fetched "+str(len(objects))+" objects")

sum=0

for i in objects:
	weight=i[indexWeight]
	sum+=weight

print("Sum of weights is "+str(sum))

average=sum/bins

print("Expected weight per bin: "+str(average))

i=0

def getScore(binWeights,average):
	score=0

	for i in binWeights:
		difference=average-i
		difference*=difference
		score+=difference

	return score

score=getScore(binWeights,average)

print("Initial score: "+str(score))

def getRandomObject(objects):
	value=random.randint(0,len(objects)-1)
	if value%2==1:
		value-=1
	return value

def getRandomBin(binWeights):
	value=random.randint(0,len(binWeights)-1)
	return value

iteration=0
lastPrint=0
printPeriod=10000
maximumIterationsWithoutImprovement=10000000
beforeStop=maximumIterationsWithoutImprovement
changes=0
lastChange=0
arrivalPeriod=0
sumOfArrivals=0
averageArrival=0

while beforeStop>=0:

	beforeStop-=1

	objectA=getRandomObject(objects)
	objectB=getRandomObject(objects)
	weightA=objects[objectA][indexWeight]
	weightB=objects[objectB][indexWeight]
	binA=objects[objectA][indexBin]
	binB=objects[objectB][indexBin]

	binWeights[binA]-=2*weightA
	binWeights[binB]-=2*weightB

	newBinA=getRandomBin(binWeights)
	newBinB=getRandomBin(binWeights)

	binWeights[newBinA]+=2*weightA
	binWeights[newBinB]+=2*weightB

	newScore=getScore(binWeights,average)

	if iteration>= lastPrint+printPeriod:
		print("Iteration: "+str(iteration)+" score: "+str(score)+" left: "+str(beforeStop)+" changes: "+str(changes)+" arrival: "+str(averageArrival))
		lastPrint=iteration

# revert the swap
	if newScore>=score:
		binWeights[newBinA]-=2*weightA
		binWeights[newBinB]-=2*weightB
		binWeights[binA]+=2*weightA
		binWeights[binB]+=2*weightB
		iteration+=1
		continue

	score=newScore
	beforeStop=maximumIterationsWithoutImprovement
	arrivalPeriod=iteration-lastChange

	changes+=2

	sumOfArrivals+=arrivalPeriod
	averageArrival=sumOfArrivals/(changes/2)
	lastChange=iteration

	objects[objectA][indexBin]=newBinA
	objects[objectA+1][indexBin]=newBinA
	objects[objectB][indexBin]=newBinB
	objects[objectB+1][indexBin]=newBinB

	lastImprovement=iteration
	iteration+=1

print("Solution:")

print("Bin	ExpectedWeight	ActualWeight")

while i<bins:
	print(str(i)+"	"+str(average)+"	"+str(binWeights[i]))
	i+=1


files={}

for i in objects:
	bin=i[indexBin]
	if bin not in files:
		files[bin]=open(inputFile+".Bin_"+str(bin)+".txt","w")

	files[bin].write(i[indexName]+"\n")


for i in files:
	files[i].close()

