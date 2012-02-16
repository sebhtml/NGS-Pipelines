#!/usr/bin/python

# write files with only unique entries

import sys

files=[]

i=1

while i<len(sys.argv):
	files.append(sys.argv[i])
	i+=1

filter={}

def entryToString(entry):
	return entry[0]+entry[1]+entry[3]+entry[4]

# count each variation
for file in files:
	for line in open(file):
		if line[0]=='#':
			continue

		entry=line.split()
		key=entryToString(entry)
		if key not in filter:
			filter[key]=0
		filter[key] += 1

# create files with unique entries
for file in files:
	out=open(file+".unique","w+")
	for line in open(file):
		if line[0]=='#':
			out.write(line)
			continue

		entry=line.split()
		key=entryToString(entry)
		# unique
		if filter[key] == 1:
			out.write(line)
	out.close()
