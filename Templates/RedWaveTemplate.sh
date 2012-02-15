##!/bin/bash
#$ -N __SAMPLE__-RedWave-2011-12-23.1
#$ -P nne-790-ab
#$ -l h_rt=48:00:00
#$ -pe default 8
#$ -cwd

source /rap/nne-790-ab/software/NGS-Pipelines/LoadModules.sh

RedWave Reference.fasta __SAMPLE__ 8 __SAMPLE__-RedWave-2011-12-23.1
