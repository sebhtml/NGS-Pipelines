#!/bin/bash
# author: Sébastien Boisvert
# date: 2011-12-23

# this is some heavy scripting
# parallel machines in bash
# I use variable indirection

referenceFileOrigin=$1
referenceFile=Reference/reference.fasta

# the argument must not be absolute paths.
sampleDirectoryOrigin=$2
sampleDirectory=sampleDirectory
processors=$3
output=$4

# run a command on a processor
runCommand(){
	processor=$1
	command=$2

	# log the command
	echo $command >> Logs/Processor$processor.txt

	echo ""
	echo "BEGIN $(date)"
	echo "running in $(pwd)"
	echo "command= $command"
	eval $command
	echo "END $(date)"
	
}

# run a group of commands on all processors
runGroupCommands(){
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
		runCommand $processorNumber "$command"
		) &

	done

	# wait for completion

	wait
}

# purge cache for a group of commands
purgeGroupCache(){
	directory=$1

	for i in $(ls $directory)
	do
		cacheFile=$(readlink $directory/$i|basename)

		if test -e $cache/$cacheFile
		then
			runCommand 0 "rm $cache/$cacheFile"
			runCommand 0 "ln -s /dev/null $cache/$cacheFile"
		fi
	done
}

mkdir $output

cd $output

mkdir Logs

runCommand 0 "mkdir Reference"

runCommand 0 "ln -s ../$referenceFileOrigin Reference.fasta"
runCommand 0 "ln -s ../Reference.fasta $referenceFile"
runCommand 0 "ln -s ../$sampleDirectoryOrigin $sampleDirectory"

runCommand 0 "mkdir meta"

cache=ApplicationCache

runCommand 0 "mkdir $cache"

runCommand 0 "bash --version &> meta/bash.version"
runCommand 0 "samtools &> meta/samtools.version"
runCommand 0 "bcftools &> meta/bcftools.version"
runCommand 0 "bwa &> meta/bwa.version"
runCommand 0 "samstat -help &> meta/samstat.version"
runCommand 0 "date > meta/date"
runCommand 0 "uname -a > meta/uname"
runCommand 0 "hostname > meta/hostname"





# for bwa
runCommand 0 "bwa index $referenceFile"

# for samtools
runCommand 0 "samtools faidx $referenceFile"

# move index file in the cache
for i in $(ls $referenceFile.*)
do
	randomFile=$(head /dev/urandom|sha1sum|awk '{print $1}')
	runCommand 0 "mv $i $cache/$randomFile"
	runCommand 0 "ln -s ../$cache/$randomFile $i"
done


# we have <processors> processors
# and we have n files
# the command is  bwa aln reference reads > sai
# we have to generate some variables

fileNumber=0

runCommand 0 "mkdir BinaryAlignments"

# generate alignments
for file in $(ls $sampleDirectory)
do
	processorNumber=$(($fileNumber%$processors))
	randomFile=$(head /dev/urandom|sha1sum|awk '{print $1}')
	command="( bwa aln $referenceFile $sampleDirectory/$file > $cache/$randomFile ) ; ( ln -s ../$cache/$randomFile BinaryAlignments/$file.sai ) ; "

	processorVariable=processor$processorNumber"BinaryAlignments"
	oldValue=$(eval echo \$$processorVariable)

	newValue=$oldValue$command

	toEval="$processorVariable=\"$newValue\""

	eval $toEval

	fileNumber=$(($fileNumber+1))
done

runGroupCommands "BinaryAlignments"


fileNumber=0
runCommand 0 "mkdir SamAlignments"

# generate compressed sam files
for fileR1 in $(ls $sampleDirectory|grep R1)
do
	fileR2=$(echo $fileR1|sed 's/R1/R2/g')
	fileRX=$(echo $fileR1|sed 's/R1/RX/g')

	randomFile=$(head /dev/urandom|sha1sum|awk '{print $1}')

	processorNumber=$(($fileNumber%$processors))
	command=" ( bwa sampe $referenceFile BinaryAlignments/$fileR1.sai BinaryAlignments/$fileR2.sai $sampleDirectory/$fileR1 $sampleDirectory/$fileR2 |gzip > $cache/$randomFile ) ; (ln -s ../$cache/$randomFile SamAlignments/$fileRX.sam.gz ) ; "
	

	processorVariable=processor$processorNumber"SamAlignments"
	oldValue=$(eval echo \$$processorVariable)

	newValue=$oldValue$command
	toEval="$processorVariable=\"$newValue\""

	eval $toEval

	fileNumber=$(($fileNumber+1))
done

runGroupCommands "SamAlignments"

purgeGroupCache "BinaryAlignments"


# do the quality control

fileNumber=0

runCommand 0 "mkdir QualityControls"

# generate compressed sam files
for samFile in $(ls SamAlignments|grep sam.gz)
do
	processorNumber=$(($fileNumber%$processors))

	randomFile=$(head /dev/urandom|sha1sum|awk '{print $1}')

	command=" ( zcat SamAlignments/$samFile | samstat -f sam -n QualityControls/$samFile) ; (mv QualityControls/$samFile.html $cache/$randomFile ) ; ( ln -s ../$cache/$randomFile QualityControls/$samFile.html ) "
	
	processorVariable=processor$processorNumber"QualityControls"
	oldValue=$(eval echo \$$processorVariable)

	newValue=$oldValue$command

	toEval="$processorVariable=\"$newValue\""

	eval $toEval

	fileNumber=$(($fileNumber+1))
done

runGroupCommands "QualityControls"




# at this point, we have a .sam.gz file for each pair
# now we need to generate sorted bam files

fileNumber=0

runCommand 0 "mkdir BamAlignments"

# generate compressed sam files
for samFile in $(ls SamAlignments|grep sam.gz)
do
	processorNumber=$(($fileNumber%$processors))

	randomFile=$(head /dev/urandom|sha1sum|awk '{print $1}')

	command=" ( samtools view -bS SamAlignments/$samFile > $cache/$randomFile ) ; (ln -s ../$cache/$randomFile BamAlignments/$samFile.bam ) ; "

	processorVariable=processor$processorNumber"BamAlignments"
	oldValue=$(eval echo \$$processorVariable)

	newValue=$oldValue$command

	toEval="$processorVariable=\"$newValue\""

	eval $toEval

	fileNumber=$(($fileNumber+1))
done

runGroupCommands "BamAlignments"

purgeGroupCache "SamAlignments"

fileNumber=0

runCommand 0 "mkdir SortedBamAlignments"

# generate compressed sam files
for samFile in $(ls SamAlignments|grep sam.gz)
do
	processorNumber=$(($fileNumber%$processors))

	randomFile=$(head /dev/urandom|sha1sum|awk '{print $1}')

	command="( samtools sort BamAlignments/$samFile.bam $cache/$randomFile ) ; ( mv $cache/$randomFile.bam $cache/$randomFile) ; (ln -s ../$cache/$randomFile SortedBamAlignments/$samFile.sorted.bam )"

	processorVariable=processor$processorNumber"SortedBamAlignments"
	oldValue=$(eval echo \$$processorVariable)

	newValue=$oldValue$command

	toEval="$processorVariable=\"$newValue\""

	eval $toEval

	fileNumber=$(($fileNumber+1))
done

runGroupCommands "SortedBamAlignments"

purgeGroupCache "BamAlignments"


# generate variation calls
fileNumber=0

runCommand 0 "mkdir Variations"
	
randomFile=$(head /dev/urandom|sha1sum|awk '{print $1}')

command=" ( samtools mpileup -uf $referenceFile $(find SortedBamAlignments|grep sorted.bam) | bcftools view -bvcg - > $cache/$randomFile ) ; ( ln -s ../$cache/$randomFile Variations/var.raw.bcf ) ; "

runCommand 0 "$command"

purgeGroupCache "Reference"

randomFile=$(head /dev/urandom|sha1sum|awk '{print $1}')

command="( bcftools view Variations/var.raw.bcf > $cache/$randomFile ) ; (ln -s ../$cache/$randomFile Variations/var.raw.vcf ) ; "

runCommand 0 "$command"

