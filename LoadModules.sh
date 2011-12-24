
# this script probably only works on colosse


export PATH=/rap/nne-790-ab/software/NGS-Pipelines:$PATH

# for RedWave

export PATH=/rap/nne-790-ab/software/bwa-0.6.1:$PATH
export PATH=/rap/nne-790-ab/software/samtools-0.1.18:$PATH
export PATH=/rap/nne-790-ab/software/samtools-0.1.18/bcftools:$PATH
export PATH=/rap/nne-790-ab/software/samstat-1.08/src:$PATH


# for VioletRay

module load compilers/gcc/4.6.1
module load mpi/openmpi/1.4.3_gcc
export PATH=/rap/nne-790-ab/software/VioletRay/ray/build-2011-12-23:$PATH


# for OrangeSpark

export PATH=/rap/nne-790-ab/software/bowtie2-2.0.0-beta5:$PATH
