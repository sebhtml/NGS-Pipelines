#!/usr/bin/python

import sys

data={}

total=0


for line in sys.stdin:
	tokens=line.split()
	x=int(tokens[0])
	y=int(tokens[1])
	total += y
	data[x]=y

maxX=None
maxY=None
maximum=None

for i in data.items():
	x=i[0]
	y=i[1]

	if maxY==None:
		maxX=x
		maxY=y
		maximum=x

	if y > maxY:
		maxX=x
		maxY=y

	if x > maximum:
		maximum=x


leftX=maxX
rightX=maxX
lastLeft=None
lastRight=None
sum=0

while leftX>=1 or rightX <= maximum:

	if leftX in data and lastLeft==None:
		sum+=data[leftX]
		lastLeft=leftX

	if leftX!=rightX and rightX in data and lastRight==None:
		sum+=data[rightX]
		lastRight=rightX

	ratio=(0.0+sum)/total*100
	
	print str(leftX)+"	"+str(rightX)+"	"+str(ratio)

	if leftX==1 and rightX==maximum:
		break

	if leftX > 1:
		leftX-=1
		lastLeft=None

	if rightX < maximum:
		rightX+=1
		lastRight=None
