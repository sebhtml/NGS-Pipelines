#!/bin/bash
#PBS -N Sample_CQDM2-3-2013-02-19-1
#PBS -o Sample_CQDM2-3-2013-02-19-1.o
#PBS -e Sample_CQDM2-3-2013-02-19-1.e
#PBS -A nne-790-ac
#PBS -l walltime=16:00:00
#PBS -l nodes=32:ppn=8
#PBS -q default
cd $PBS_O_WORKDIR

source /rap/nne-790-ab/software/NGS-Pipelines/LoadModules.sh

mpiexec -n 128 \
Ray -k 61 -o Sample_CQDM2-3-2013-02-19-1 \
-write-seeds \
-write-extensions \
-write-kmers \
-p \
 Sample_CQDM2-3/CQDM2-3_Lane5_R1_1.fastq.gz \
 Sample_CQDM2-3/CQDM2-3_Lane5_R2_1.fastq.gz \
-p \
 Sample_CQDM2-3/CQDM2-3_Lane5_R1_2.fastq.gz \
 Sample_CQDM2-3/CQDM2-3_Lane5_R2_2.fastq.gz \
-p \
 Sample_CQDM2-3/CQDM2-3_Lane5_R1_3.fastq.gz \
 Sample_CQDM2-3/CQDM2-3_Lane5_R2_3.fastq.gz \
-p \
 Sample_CQDM2-3/CQDM2-3_Lane5_R1_4.fastq.gz \
 Sample_CQDM2-3/CQDM2-3_Lane5_R2_4.fastq.gz \
-p \
 Sample_CQDM2-3/CQDM2-3_Lane5_R1_5.fastq.gz \
 Sample_CQDM2-3/CQDM2-3_Lane5_R2_5.fastq.gz \
-p \
 Sample_CQDM2-3/CQDM2-3_Lane5_R1_6.fastq.gz \
 Sample_CQDM2-3/CQDM2-3_Lane5_R2_6.fastq.gz \
