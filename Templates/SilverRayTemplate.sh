#!/bin/bash
#PBS -N __SAMPLE__+Ray-2012-08-29-system-test-289
#PBS -o __SAMPLE__+Ray-2012-08-29-system-test-289.stdout
#PBS -e __SAMPLE__+Ray-2012-08-29-system-test-289.stderr
#PBS -A nne-790-ab
#PBS -l walltime=16:00:00
#PBS -l nodes=4:ppn=8
cd "${PBS_O_WORKDIR}"

source /rap/nne-790-ab/software/NGS-Pipelines/LoadModules.sh

SilverRay 31 __SAMPLE__ 32 __SAMPLE__+Ray-2012-08-29-system-test-289
