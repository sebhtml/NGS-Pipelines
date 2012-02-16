import math

reads=[]
for line in open('../../numberOfReads.txt'):
	reads.append(int(line))

files=[]
files.append("20100916_708YKAAXX_s1_r1_iall.fastq.sam.bz2.windows")
files.append("20100916_708YKAAXX_s2_r1_iall.fastq.sam.bz2.windows")
files.append("20100916_708YKAAXX_s3_r1_iall.fastq.sam.bz2.windows")
files.append("20100916_708YKAAXX_s4_r1_iall.fastq.sam.bz2.windows")
files.append("20100916_708YKAAXX_s5_r1_iall.fastq.sam.bz2.windows")
files.append("20100916_708YKAAXX_s6_r1_iall.fastq.sam.bz2.windows")
files.append("20100916_708YKAAXX_s7_r1_iall.fastq.sam.bz2.windows")
files.append("20100916_708YKAAXX_s8_r1_iall.fastq.sam.bz2.windows")

normData=[]

i=0
while i<len(files):
	array=[]
	ratio=reads[0]/(0.0+reads[i])
	f=open(files[i]+".norm","w+")
	for line in open(files[i]):
		tokens=line.split()
		value=ratio*int(tokens[3])
		f.write(tokens[0]+"\t"+tokens[1]+"\t"+tokens[2]+"\t"+str(value)+"\n")
		array.append(value)
	f.close()
	normData.append(array)
	i+=1

i=0
while i<len(files):
	f=open(files[i]+".log2ratio","w+")
	j=0
	for line in open(files[i]):
		tokens=line.split()
		value=math.log(normData[i][j]/normData[0][j])/math.log(2)
		f.write(tokens[0]+"\t"+tokens[1]+"\t"+tokens[2]+"\t"+str(value)+"\n")
		j+=1
	f.close()
	i+=1

