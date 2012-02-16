#!/usr/bin/python

import sys
files=[]

i=1
while i<len(sys.argv):
	files.append(sys.argv[i])
	i+=1

theLargeDataStructureThatNeedsPeriodicUpdatesOrItDies={}

theName=1

# LmjF.01.0250    188     GeneDB|LmjF.01  65798   .       A       G       164     .       DP=51;VDB=0.0474;AF1=1;AC1=2;DP4=0,0,30,19;MQ=37;FQ=-175        GT:PL:GQ        1/1:197,148,0:99        CTT     CCT     L       P


for i in files:
	for j in open(i):
		tokens=j.split()
		gene=tokens[0]
		position=tokens[1]
		chromosome=tokens[2]
		largePosition=tokens[3]
		reference=tokens[5]
		consensus=tokens[6]
		key=gene+" "+position+" ("+chromosome+" "+largePosition+")"
		if key not in theLargeDataStructureThatNeedsPeriodicUpdatesOrItDies:
			theLargeDataStructureThatNeedsPeriodicUpdatesOrItDies[key]={}
		theLargeDataStructureThatNeedsPeriodicUpdatesOrItDies[key][theName]=j
	theName+=1


sortedKeys=theLargeDataStructureThatNeedsPeriodicUpdatesOrItDies.keys()
sortedKeys.sort()

#     * wild-type 1
#     * SbIII 2-4
#     * miltefosine 5,6
#     * paramomycin 7,8 


writers={}
for i in files:
	f=open(i+".3","w+")
	writers[i]=f

print "<html><head><style>table{border-collapse:collapse;} td{ border:1px solid black;}</style></head><body>"

print "<table>"
for i in sortedKeys:
	population=len(theLargeDataStructureThatNeedsPeriodicUpdatesOrItDies[i])
	wildType=0
	sbIII=0
	miltefosine=0
	paramomycin=0
	if 1 in theLargeDataStructureThatNeedsPeriodicUpdatesOrItDies[i]:
		wildType+=1
	if 2 in theLargeDataStructureThatNeedsPeriodicUpdatesOrItDies[i]:
		sbIII=1
	if 3 in theLargeDataStructureThatNeedsPeriodicUpdatesOrItDies[i]:
		sbIII=1
	if 4 in theLargeDataStructureThatNeedsPeriodicUpdatesOrItDies[i]:
		sbIII=1
	if 5 in theLargeDataStructureThatNeedsPeriodicUpdatesOrItDies[i]:
		miltefosine=1
	if 6 in theLargeDataStructureThatNeedsPeriodicUpdatesOrItDies[i]:
		miltefosine=1
	if 7 in theLargeDataStructureThatNeedsPeriodicUpdatesOrItDies[i]:
		paramomycin=1
	if 8 in theLargeDataStructureThatNeedsPeriodicUpdatesOrItDies[i]:
		paramomycin=1

	count=wildType+sbIII+miltefosine+paramomycin

	if count>1:
		continue
	if wildType>0:
		continue

	if population==len(files):
		continue
	if population==len(files)-1:
		continue

	theName=1
	print "<tr><td>"+i+"</td>"
	for j in files:
		if theName==1:
			theName+=1
			continue

		output=""
		if theName in theLargeDataStructureThatNeedsPeriodicUpdatesOrItDies[i]:
			print "<td style=\"background-color: yellow;\">"+str(theName)+"</td>"
			writers[j].write(theLargeDataStructureThatNeedsPeriodicUpdatesOrItDies[i][theName])
		else:
			print "<td>"+str(theName)+"</td>"
		theName+=1
	print "</tr>"
print "</table>"
			

for i in writers.items():
	i[1].close()
