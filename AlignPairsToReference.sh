#!/bin/bash

# this is some heavy scripting
# parallel machines in bash
# I use variable indirection

referenceFile=$1
sampleDirectory=$2
processors=$3

runCommand(){
	command=$1
	echo ""
	echo "BEGIN $(date)"
	echo "running supplied command without callback"
	echo "command= $command"
	#$command
	echo "END $(date)"
}

runCommands(){
	commandGroup=$1

	echo ""
	echo "Initiating command group: $commandGroup"
	echo "Using $processors processors"
	echo ""

	# actually do the conversion
	for processorNumber in $(seq 0 $((processors-1)))
	do
		(
		echo ""
		echo "Processor $processorNumber"
		processorVariable=processor$processorNumber$commandGroup
		echo "processorVariable= $processorVariable"
		command=$(eval echo \$$processorVariable)
		#command=DEBUG$commandGroup$processorNumber
		runCommand "$command"
		) &

	done

	# wait for completion

	wait
}


# for bwa
runCommand "bwa index $referenceFile"

# for samtools
runCommand "samtools faidx $referenceFile"

numberOfFiles=$(ls $sampleDirectory|grep fastq|wc -l)

# we have <processors> processors
# and we have $numberOfFiles files
# the command is  bwa aln reference reads > sai
# we have to generate some variables

fileNumber=0

runCommand "mkdir SaiCommands"

# generate alignments
for file in $(ls $sampleDirectory)
do
	processorNumber=$(($fileNumber%$processors))
	command="bwa aln $referenceFile $sampleDirectory/$file>SaiCommands/$file.sai;"

	processorVariable=processor$processorNumber"SaiCommands"
	oldValue=$(eval echo \$$processorVariable)

	newValue=$oldValue$command

	toEval="$processorVariable=\"$newValue\""

	eval $toEval

	fileNumber=$(($fileNumber+1))
done

runCommands "SaiCommands"

fileNumber=0

runCommands "mkdir SamCommands"

# generate compressed sam files
for fileR1 in $(ls $sampleDirectory|grep R1)
do
	fileR2=$(echo $fileR1|sed 's/R1/R2/g')

	processorNumber=$(($fileNumber%$processors))
	command="bwa sampe $referenceFile $sampleDirectory/$fileR1.sai $sampleDirectory/$fileR2.sai  $sampleDirectory/$fileR1 $sampleDirectory/$fileR2 |gzip > SamCommands/$file.sam.gz;"
	
	processorVariable=processor$processorNumber"SamCommands"
	oldValue=$(eval echo \$$processorVariable)

	newValue=$oldValue$command

	toEval="$processorVariable=\"$newValue\""

	eval $toEval

	newValue=$(eval echo \$$processorVariable)

	fileNumber=$(($fileNumber+1))
done

runCommands "SamCommands"

# at this point, we have a .sam.gz file for each pair
# now we need to generate sorted bam files

fileNumber=0

runCommands "mkdir BamCommands"

# generate compressed sam files
for samFile in $(ls Alignments|grep sam.gz)
do
	processorNumber=$(($fileNumber%$processors))

	command="samtools view -o BamCommands/$samFile.bam SamCommands/$samFile;"
	command=$command"samtools sort BamCommands/$samFile.bam BamCommands/$samFile.sorted;"

	processorVariable=processor$processorNumber"BamCommands"
	oldValue=$(eval echo \$$processorVariable)

	newValue=$oldValue$command

	toEval="$processorVariable=\"$newValue\""

	eval $toEval

	newValue=$(eval echo \$$processorVariable)

	fileNumber=$(($fileNumber+1))
done

runCommands "BamCommands"


# generate variation calls
fileNumber=1

runCommand "mkdir VcfCommands"

command="samtools mpileup -uf reference.fasta $(find BamCommands|grep sorted.bam) | bcftools view -bvcg - > VcfCommands/var.raw.bcf"

runCommand $command

command="bcftools view VcfCommands/var.raw.bcf > VcfCommands/var.raw.vcf"


runCommand $command


ln -s SaiCommands BinaryAlignments
ln -s SamCommands Alignments
ln -s BamCommands SortedAlignments
ln -s VcfCommands Variations
