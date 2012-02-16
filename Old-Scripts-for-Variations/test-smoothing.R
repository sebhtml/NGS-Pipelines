#!/usr/bin/Rscript

# script that makes beautiful graphics.
# author: Sébastien Boisvert

library(methods)
library(limma)

arguments=commandArgs()

numberOfReads=read.table("numberOfReads.txt")[[1]]

theWidth=1500
theHeight=1000
theColor="black"

getImageContent=function(image,title){
	paste("<div style=\"background: #CAFF70; border-style: solid; text-align: center; padding: 0.3cm;\"><div style=\"padding: 1cm;\"><u>",title,"</u><br /></div><img src=\"",image,"\" style=\"border-style: solid;\"/></div><br />",sep="")
}


for(sample in c(__SAMPLE__)){
	for(chromosome in c(__CHROMOSOME__)){
		print(paste("Starting computation for sample ",sample,", chromosome ",chromosome,sep=""))
		content=""
		sample1=numberOfReads[1]
		thisSample=numberOfReads[sample]
		normalizationRatio=sample1/thisSample
		content=paste(content,"Sample: ",sep="")
		for(sample2 in 1:8){
			content=paste(content,"<a href=\"",sample2,"-",chromosome,".html\">",sample2,"</a> ",sep="")
		}
		content=paste(content,"<br />",sep="")

		content=paste(content,"Chromosome: ",sep="")
		for(chromosome2 in 1:36){
			content=paste(content,"<a href=\"",sample,"-",chromosome2,".html\">",chromosome2,"</a> ",sep="")
		}
		content=paste(content,"<br />",sep="")

		
		content=paste(content,"<h1>Sample ",sample,", chromosome ",chromosome,"</h1>",sep="")

		coverageFor1=read.table(paste("20100916_708YKAAXX_s",1,"_r1_iall.fastq.sam-",chromosome,".cov",sep=""))
		coverage=paste("20100916_708YKAAXX_s",sample,"_r1_iall.fastq.sam-",chromosome,".cov",sep="")
		coverageSample1=paste("20100916_708YKAAXX_s",1,"_r1_iall.fastq.sam-",chromosome,".cov",sep="")
		coverageData=read.table(coverage)
		coverageData1=read.table(coverageSample1)
		
		contentFile=paste("",chromosome,".GC",sep="")
		contentData=read.table(contentFile)
		x=contentData[[3]]
		y=coverageData[[3]]
		data=data.frame(x=x,y=y)
		fit=loessFit(y,x)
		fit1=loessFit(coverageData1[[3]],x)
		meanCoverage=mean(y)
		deviation=sd(y)
		minGC=min(x)
		maxGC=max(x)
		
		meanCoverage=mean(coverageData[[3]])
		meanCoverage1=mean(coverageData1[[3]])
		deviationCoverage=sd(coverageData[[3]])

		# coverage distribution
		distributionOfTheNumberOfReads=paste("Sample",sample,"Chromosome",chromosome,"-DistributionOfTheNumberOfReads.png",sep="")
		png(distributionOfTheNumberOfReads,width=theWidth,height=theHeight)
		plot(hist(coverageData[[3]],breaks=1000),xlab='Number of reads',ylab='Count',main='Distribution of the number of reads',xlim=c(0,300))
		dev.off()

		add=getImageContent(distributionOfTheNumberOfReads,"Distribution of the number of reads")
		content=paste(content,add)

		# GC distribution
		distributionOfTheNumberGCContent=paste("Sample",sample,"Chromosome",chromosome,"-DistributionOfGCContent.png",sep="")
		png(distributionOfTheNumberGCContent,width=theWidth,height=theHeight)
		plot(hist(contentData[[3]],breaks=100),xlab='GC content',ylab='Count',main='Distribution of GC content')
		dev.off()
		content=paste(content,getImageContent(distributionOfTheNumberGCContent,"Distribution of GC content"))


		# raw reads

		rawReadsVGCContentFile=paste("Sample",sample,"Chromosome",chromosome,"-RawReads.png",sep="")
		png(rawReadsVGCContentFile,width=theWidth,height=theHeight)
		main="Number of reads on the chromosome"
		plot(coverageData[[2]],coverageData[[3]],type='l',col=theColor,xlab='Nucleotide position',ylab='Number of reads',ylim=c(0,300),main=main)
		dev.off()

		content=paste(content,getImageContent(rawReadsVGCContentFile,main))

		#  with GC content
		gcContentFile=paste("Sample",sample,"Chromosome",chromosome,"-GCContent.png",sep="")
		png(gcContentFile,width=theWidth,height=theHeight)
		main="GC content on the chromosome"
		plot(contentData[[2]],contentData[[3]],type='l',col=theColor,xlab='Nucleotide position',ylab='GC content',main=main)
		dev.off()

		content=paste(content,getImageContent(gcContentFile,main))

		# scatter plot
		scatterPlotFile=paste("Sample",sample,"Chromosome",chromosome,"-ScatterPlot.png",sep="")
		png(scatterPlotFile,width=theWidth,height=theHeight)
		main='Number of reads v. GC content, window length is 5kb'
		plot(x,y,xlab='GC content',ylab='Number of reads',main=main,ylim=c(0,300),pch=20,col=theColor)
		lines(x,fit$fitted,col='red')
		dev.off()

		content=paste(content,getImageContent(scatterPlotFile,main))


		# scatter plot normalized
		scatterPlotFileNormalized=paste("Sample",sample,"Chromosome",chromosome,"-NormalizedScatterPlot.png",sep="")
		png(scatterPlotFileNormalized,width=theWidth,height=theHeight)
		yNormalized=y+(meanCoverage-fit$fitted)
		yNormalized1=coverageData1[[3]]+(meanCoverage1-fit1$fitted)
		main='Number of reads v. GC content (normalized)'

		plot(x,yNormalized,xlab='GC content',ylab='Number of reads',main=main,ylim=c(0,300),pch=20,col=theColor)
		lines(c(minGC,maxGC),c(meanCoverage,meanCoverage),col='red')
		dev.off()


		content=paste(content,getImageContent(scatterPlotFileNormalized,main))

		# raw reads  (normalized with GC content)

		rawReadsVGCContentFile=paste("Sample",sample,"Chromosome",chromosome,"-RawReadsNormalizedGC.png",sep="")
		png(rawReadsVGCContentFile,width=theWidth,height=theHeight)
		main="Number of reads on the chromosome (normalized with GC content, blue is raw)"
		plot(coverageData[[2]],y,type='l',xlab='Nucleotide position',ylab='Number of reads',ylim=c(0,300),main=main,col='blue')
		lines(coverageData[[2]],yNormalized,col='black')
		dev.off()
		content=paste(content,getImageContent(rawReadsVGCContentFile,main))

		# reads normalized with GC content and with sample 1

		rawReadsVGCContentFile=paste("Sample",sample,"Chromosome",chromosome,"-RawReadsNormalizedGCNormalizedAgainst1.png",sep="")
		png(rawReadsVGCContentFile,width=theWidth,height=theHeight)
		normalizedPoints=yNormalized*normalizationRatio
		main="Number of reads on the chromosome (normalized with GC content and against sample 1, blue is sample 1)"
		plot(coverageData[[2]],yNormalized1,type='l',xlab='Nucleotide position',ylab='Number of reads',ylim=c(0,300),main=main,col='blue')
		lines(coverageData[[2]],normalizedPoints,col='black')
		dev.off()
		content=paste(content,getImageContent(rawReadsVGCContentFile,main))


		cat(content,file=paste(sample,"-",chromosome,".html",sep=""))

		print(paste("Ending computation for sample ",sample,", chromosome ",chromosome,sep=""))

	}
}

system("cp 1-1.html index.html")
