#!/usr/bin/env Rscript
# Sébastien Boisvert
# license: GPLV3

# based on http://www.snl.salk.edu/~shlens/pca.pdf

arguments=commandArgs(trailingOnly = TRUE)

if(length(arguments) != 2){
	print("incorrect usage")
	print("usage")
	print("")
	print("PrincipalComponentAnalysis.R <matrix> <method>")
	print("  <matrix is a tab-separated file with attributes as rows and samples as columns, with headers and first column as attribute names")
	print("  <method> is eigen or svd")
	print("")
	print("Outputs")
	print(" data=<matrix>,method=<method>.pdf")

	print("Example:")
	print("PrincipalComponentAnalysis.R Matrix.txt svd")
	print("PrincipalComponentAnalysis.R Matrix.txt eigen")
	print("PrincipalComponentAnalysis.R Matrix.txt svd")
	quit()
}

minimumProportion=0

file=arguments[1]
method=arguments[2]
component1=1
component2=2



# load the file
data=as.matrix(read.table(file,header=TRUE,row.names=1,sep="\t"))

#  get dimensions
columns=length(data[1,])
rows=length(data[,1])

group1=columns
group2=0

prefix=paste("data=",file,",method=",method,",component1=",component1,",component2=",component2,",",group1,",",group2,sep="")

cat("method= ",method," rows= ",rows," columns= ",columns," group1= ",group1," group2= ",group2,"\n")

# compute the mean for each row
# and center points to 0
i=1

centeredData=data

while(i<=rows){

	averageValue=mean(data[i,])
	
	#cat("Average ",averageValue,"\n")

	if(averageValue < minimumProportion){
		centeredData[i,] = data[i,] - data[i,]
	}else{
		centeredData[i,] = data[i,] - averageValue
	}

	i=i+1
}

# 1. Using eigen vectors

# calculate the covariance matrix

covariance = 1 / (rows-1) * centeredData %*% t(centeredData)

#print(covariance)

# get eigen vectors

eigenOutput = eigen(covariance)

#print(eigenOutput)

#summary(eigenOutput)

eigenValues=eigenOutput$values
eigenVectors=eigenOutput$vectors

principalComponents=c()

if(method=='eigen'){
	principalComponents=eigenVectors
}




# 2. singular value decomposition

newRepresentation = t(centeredData) / sqrt(rows-1)
svdOutput = svd(newRepresentation)

if(method=='svd'){
	# use rhe right matrix
	principalComponents=svdOutput$v 

	# why not use the left matrix
	#principalComponents=t(svdOutput$u)
}





# rotate and stretch
signals = t(principalComponents) %*% centeredData

pdf(paste(prefix,".pdf",sep=""))

x=signals[component1,]
y=signals[component2,]

plot(x[1:group1],y[1:group1],main=paste("Method= ",method),col='red',
xlim=c(min(x),max(x)),
ylim=c(min(y),max(y)))

points(x[group1+1:columns],y[group1+1:columns],main=paste("Method= ",method),col='black')

dev.off()

write.table(signals,file=paste(prefix,".re-representation.txt",sep=""),sep="\t")
write.table(principalComponents,file=paste(prefix,".baseVectors.txt",sep=""),sep="\t")
