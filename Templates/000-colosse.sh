#!/bin/bash
#PBS -N RayRay-__SAMPLE__-2013-01-01-1
#PBS -o RayRay-__SAMPLE__-2013-01-01-1.stdout
#PBS -e RayRay-__SAMPLE__-2013-01-01-1.stderr
#PBS -A nne-790-ac
#PBS -l walltime=16:00:00
#PBS -l nodes=8:ppn=8
#PBS -q default

cd $PBS_O_WORKDIR

echo $PBS_JOBID > RayRay-__SAMPLE__-2013-01-01-1.job

module load compilers/gcc/4.8.0
module load apps/blcr/0.8.4
module load mpi/openmpi/1.6.4_gcc

mpiexec -n 64 \
Ray -k 31 -o RayRay-__SAMPLE__-2013-01-01-1.job \
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
