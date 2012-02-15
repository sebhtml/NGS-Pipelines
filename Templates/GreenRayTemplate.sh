#!/bin/bash
#PBS -N __SAMPLE__-Ray-2012-02-14-Sheldon
#PBS -l nodes=3:ppn=12
#PBS -q hb
#PBS -l walltime=8:00:00

cd /home/sboisver12/nne-790-ab/projects/Qin-et-al

source /sb/project/nne-790-ab/software/NGS-Pipelines/LoadModules.sh

VioletRay 31 __SAMPLE__ 36 __SAMPLE__-Ray-2012-02-14-Sheldon
