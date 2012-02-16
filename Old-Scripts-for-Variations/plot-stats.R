#!/usr/bin/Rscript

r1=read.table('20100916_708YKAAXX_s1_r1_iall.fastq.varFilter.unique.stats')
r2=read.table('20100916_708YKAAXX_s2_r1_iall.fastq.varFilter.unique.stats')
r3=read.table('20100916_708YKAAXX_s3_r1_iall.fastq.varFilter.unique.stats')
r4=read.table('20100916_708YKAAXX_s4_r1_iall.fastq.varFilter.unique.stats')
r5=read.table('20100916_708YKAAXX_s5_r1_iall.fastq.varFilter.unique.stats')
r6=read.table('20100916_708YKAAXX_s6_r1_iall.fastq.varFilter.unique.stats')
r7=read.table('20100916_708YKAAXX_s7_r1_iall.fastq.varFilter.unique.stats')
r8=read.table('20100916_708YKAAXX_s8_r1_iall.fastq.varFilter.unique.stats')

pdf("VariationsOnChromosomes.pdf",width=200,height=800)
par(mfrow=c(8,1))

plot(r1[[1]],r1[[2]],type='h',xlab='Chromosome',ylab='Number of variations',main="Sample 1")
plot(r2[[1]],r2[[2]],type='h',xlab='Chromosome',ylab='Number of variations',main="Sample 2")
plot(r3[[1]],r3[[2]],type='h',xlab='Chromosome',ylab='Number of variations',main="Sample 3")
plot(r4[[1]],r4[[2]],type='h',xlab='Chromosome',ylab='Number of variations',main="Sample 4")
plot(r5[[1]],r5[[2]],type='h',xlab='Chromosome',ylab='Number of variations',main="Sample 5")
plot(r6[[1]],r6[[2]],type='h',xlab='Chromosome',ylab='Number of variations',main="Sample 6")
plot(r7[[1]],r7[[2]],type='h',xlab='Chromosome',ylab='Number of variations',main="Sample 7")
plot(r8[[1]],r8[[2]],type='h',xlab='Chromosome',ylab='Number of variations',main="Sample 8")

dev.off()
