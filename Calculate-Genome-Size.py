#!/usr/bin/env python
# authorship: Sebastien Boisvert
# copyright: Copyright (C) 2012 Sebastien Boisvert
# license: GNU General Public License version 3

import sys

arguments=sys.argv

if len(sys.argv)!=4:
	print("Usage: "+arguments[0]+" CoverageDistribution.txt startingCoverage endingCoverage")
	sys.exit()

file=arguments[1]

stream=open(file)

sum=0
count=0
startingCoverage=int(arguments[2])
endingCoverage=int(arguments[3])

for line in stream:
	if line[0]=='#':
		continue
	tokens=line.split()
	coverage=int(tokens[0])

	if coverage<startingCoverage:
		continue

	if coverage>endingCoverage:
		continue

	frequency=int(tokens[1])

	sum+=(coverage*frequency)
	count+=frequency
	
stream.close()

averageCoverage=sum/count

# we must divide by two because we only need one DNA strand
genomeSize=count/2

print("Starting k-mer coverage: "+str(startingCoverage))
print("Ending k-mer coverage: "+str(endingCoverage))
print("Average k-mer coverage: "+str(averageCoverage))
print("Estimated haploid genome size: "+str(genomeSize))

