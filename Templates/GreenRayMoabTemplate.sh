#!/bin/bash
#PBS -N __SAMPLE__+Ray-2012-03-29-GC-content
#PBS -A nne-790-ab
#PBS -l walltime=16:00:00
#PBS -l nodes=8:ppn=8
#PBS -q default
cd $PBS_O_WORKDIR

source /rap/nne-790-ab/software/NGS-Pipelines/LoadModules.sh

ls -l $RAY_PATH

GreenRay 31 __SAMPLE__ 64 __SAMPLE__+Ray-2012-03-29-GC-content
