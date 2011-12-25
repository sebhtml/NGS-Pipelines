##!/bin/bash
#$ -N __SAMPLE__-VioletRay-2011-12-25.1
#$ -P nne-790-ab
#$ -l h_rt=48:00:00
#$ -pe default 32
#$ -cwd

source /rap/nne-790-ab/software/NGS-Pipelines/LoadModules.sh

VioletRay 31 __SAMPLE__ 32 __SAMPLE__-VioletRay-2011-12-25.1
