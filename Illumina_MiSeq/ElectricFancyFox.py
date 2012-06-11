#!/usr/bin/env python
# Title: "Electric Fancy Fox . Python"
# encoding: utf-8
# written by sebHTML (S. Boisvert)
# 2012-06-11
# reason for creating this software:
#  the last Illumina(R) MiSeq(R) run failed to convert the data on board
# because of a faulty cluster density.

"""

The Illumina(R) MiSeq(TM) from Illumina Inc.
produces a sample sheet file on board, but it is not compatible
with Illumina(R) CASAVA.




Legal stuff.

ILLUMINA® is a registered trademark of Illumina, Inc.


<This is a Illumina(R) MiSeq(R) SampleSheet>

[Header]
IEMFileVersion,4
Investigator Name,LR
Project Name,LSPQ
Experiment Name,20120606
Date,6/6/2012
Workflow,GenerateFASTQ
Application,FASTQ Only
Assay,TruSeq DNA/RNA
Description,
Chemistry,Default

[Reads]
151
151

[Settings]

[Data]
Sample_ID,Sample_Name,Sample_Plate,Sample_Well,Sample_Project,index,I7_Index_ID,Description,GenomeFolder
90377-1,,LSPQ20120606,A01,,ATCACG,A001,,PhiX\Illumina\RTA\Sequence\WholeGenomeFASTA
90443-1,,LSPQ20120606,A02,,CGATGT,A002,,PhiX\Illumina\RTA\Sequence\WholeGenomeFASTA
90941-1,,LSPQ20120606,A03,,TTAGGC,A003,,PhiX\Illumina\RTA\Sequence\WholeGenomeFASTA
91375-1,,LSPQ20120606,A04,,TGACCA,A004,,PhiX\Illumina\RTA\Sequence\WholeGenomeFASTA
91378-1,,LSPQ20120606,A05,,ACAGTG,A005,,PhiX\Illumina\RTA\Sequence\WholeGenomeFASTA
91655-1,,LSPQ20120606,A06,,GCCAAT,A006,,PhiX\Illumina\RTA\Sequence\WholeGenomeFASTA
91664-1,,LSPQ20120606,A07,,CAGATC,A007,,PhiX\Illumina\RTA\Sequence\WholeGenomeFASTA
91845-1,,LSPQ20120606,A08,,CTTGTA,A012,,PhiX\Illumina\RTA\Sequence\WholeGenomeFASTA
92375-1,,LSPQ20120606,A09,,AGTCAA,A013,,PhiX\Illumina\RTA\Sequence\WholeGenomeFASTA
93302-1,,LSPQ20120606,A10,,AGTTCC,A014,,PhiX\Illumina\RTA\Sequence\WholeGenomeFASTA
93363-1,,LSPQ20120606,A11,,ATGTCA,A015,,PhiX\Illumina\RTA\Sequence\WholeGenomeFASTA
90494-1,,LSPQ20120606,A12,,CCGTCC,A016,,PhiX\Illumina\RTA\Sequence\WholeGenomeFASTA
90505-1,,LSPQ20120606,B01,,GTCCGC,A018,,PhiX\Illumina\RTA\Sequence\WholeGenomeFASTA
93302-2,,LSPQ20120606,B02,,GTGAAA,A019,,PhiX\Illumina\RTA\Sequence\WholeGenomeFASTA

</This is a Illumina(R) MiSeq(R) SampleSheet>


<This is a Illumina(R) CASAVA(R) SampleSheet>

FCID,Lane,SampleID,SampleRef,Index,Description,Control,Recipe,Operator,SampleProject
000000000-A0VER,1,R6_WT,,GCCAAT,,N,PE_indexing,FR,RNA-seq_spr0058_20120604
000000000-A0VER,1,R6_KOspr0058,,CTTGTA,,N,PE_indexing,FR,RNA-seq_spr0058_20120604

</This is a Illumina(R) CASAVA(R) SampleSheet>

"""

import sys

programName=sys.argv[0]

if len(sys.argv)!=3:
	print "Usage:"
	print programName+"	inputMiSeqSampleSheet	outputCASAVASampleSheet"
	sys.exit(1)

miseqSampleSheet=sys.argv[1]

output=sys.argv[2]

flowcellIdentifier="Unknown"
lane="1"
machineOperator="Unknown"
projectName="Unknown"

started=False

operationCode_Header="[Header]"
operationCode_Reads="[Reads]"
operationCode_Settings="[Settings]"
operationCode_Data="[Data]"

stream=open(output,"w")

print "Welcome to this tool."

print "I will process the MiSeq sample sheet <"+miseqSampleSheet+"> today."
stream.write("FCID,Lane,SampleID,SampleRef,Index,Description,Control,Recipe,Operator,SampleProject")
stream.write("\n")

gotHeader=False

for line in open(miseqSampleSheet):
	operationCode=line.strip()
	if operationCode==operationCode_Data:
		started=True
		continue

	if line.find("Project Name,")>=0:
		projectName=line.replace("Project Name,","").strip()
		
	if not started:
		continue

	if not gotHeader:
		gotHeader=True
		continue

	tokens=line.split(",")

	
# MiSeq format
# Sample_ID,Sample_Name,Sample_Plate,Sample_Well,Sample_Project,index,I7_Index_ID,Description,GenomeFolder
# 90377-1,,LSPQ20120606,A01,,ATCACG,A001,,PhiX\Illumina\RTA\Sequence\WholeGenomeFASTA

	sampleName=tokens[1].strip()

	# take the identifier if the name is empty.
	if sampleName=="":
		print "Warning: Sample_Name is empty, will use Sample_ID for the sample name"
		sampleName=tokens[0].strip()

	if sampleName=="":
		print "Error: sample name is empty."
		sys.exit(1)

	index=tokens[5].strip()

# CASAVA format
#FCID,Lane,SampleID,SampleRef,Index,Description,Control,Recipe,Operator,SampleProject
#000000000-A0VER,1,R6_WT,,GCCAAT,,N,PE_indexing,FR,RNA-seq_spr0058_20120604


	stream.write(flowcellIdentifier+",")
	stream.write(lane+",")
	stream.write(sampleName+",")
	stream.write(",")
	stream.write(index+",")
	stream.write(",")
	stream.write("N,")
	stream.write("PE_indexing,")
	stream.write(machineOperator+",")
	stream.write(projectName)

	stream.write("\n")
stream.close()

print "CASAVA Sample sheet file <"+output+"> is now on the disk"
print "Have a nice day."
