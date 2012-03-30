#!/bin/bash

sequence1=$1
sequence2=$2

mummer -mum -b -c -l 100 $sequence1 $sequence2 > $sequence2.mums

mummerplot -postscript -p $sequence2 $sequence2.mums -f

ps2pdf $sequence2.ps
