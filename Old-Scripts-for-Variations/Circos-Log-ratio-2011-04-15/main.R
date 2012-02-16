# Sébastien Boisvert
# 2011-04-15
# take coverage at each position and normalise things.
# 36 chromosomes
# 8 samples, 1 is wild-type

arguments=commandArgs(TRUE)

sample=as.numeric(arguments[1])
chromosome=as.numeric(arguments[2])


fileForcoverageFor1=paste("../../20100916_708YKAAXX_s",1,"_r1_iall.fastq.sam-",chromosome,".cov",sep="")
fileForjcoverage=paste("../../20100916_708YKAAXX_s",sample,"_r1_iall.fastq.sam-",chromosome,".cov",sep="")
fileForNumberOfReads='../../numberOfReads.txt'

print(paste("Reading ",fileForNumberOfReads))
numberOfReads=read.table(fileForNumberOfReads)
print(numberOfReads[[1]])
print(paste("Reading ",fileForcoverageFor1))

countsFor1=read.table(fileForcoverageFor1)
print(paste("Reading ",fileForjcoverage))
countsForCurrent=read.table(fileForjcoverage)

coverageArrayOfSample1=countsFor1[[3]]
print(paste("Entries for wild-type: ",length(coverageArrayOfSample1)))
coverageArrayOfCurrentSample=countsForCurrent[[3]]
print(paste("Entries for mutant: ",length(coverageArrayOfCurrentSample)))
numberOfReadsFor1=numberOfReads[[1]][1]
numberOfReadsForCurrentSample=numberOfReads[[1]][sample]
print(paste("Reads for wild-type: ",numberOfReadsFor1))
normalisationRatio=numberOfReadsFor1/(0.0+numberOfReadsForCurrentSample)
print(paste("Reads for mutant: ",numberOfReadsForCurrentSample))

normalisedPointsForCurrentSample=coverageArrayOfCurrentSample*normalisationRatio
normalisedPointsAgainstSample1=normalisedPointsForCurrentSample/coverageArrayOfSample1
log2Ratios=log(normalisedPointsAgainstSample1)/log(2)

write.table(data.frame(a=countsFor1[[2]],b=log2Ratios),paste("Sample-",sample,"-Chromosome-",chromosome,sep=""),col.names=FALSE,row.names=FALSE,quote=FALSE)
