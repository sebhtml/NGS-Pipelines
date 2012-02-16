#!/usr/bin/python

counts={}
for file in open("FILES.txt"):
	file=file.strip()
	for line in open(file):
		tokens=line.split()
		chromosome=tokens[0]
		position=tokens[1]
		key=chromosome+position
		if key not in counts:
			counts[key]=0
		counts[key]+=1

for file in open("FILES.txt"):
	file=file.strip()
	output=open(file+".uniq.txt","w+")
	for line in open(file):
		tokens=line.split()
		chromosome=tokens[0]
		position=tokens[1]
		key=chromosome+position
		count=counts[key]
		if count==1:
			output.write(line)
	output.close()
