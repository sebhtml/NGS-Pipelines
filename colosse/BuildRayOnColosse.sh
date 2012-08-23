#!/bin/bash

source /rap/nne-790-ab/software/NGS-Pipelines/LoadModules.sh

cd ~/git-clones/ray

id=$(git log|grep ^commit|head -n1|awk '{print $2}')
builds=/rap/nne-790-ab/software/RayAppBuilds/

make clean

make ASSERT=y DEBUG=y HAVE_LIBZ=y HAVE_LIBBZ2=y EXTRA=-march=native J=10 PREFIX=$builds/$id
make install

cd $builds
rm last-build
ln -s $id last-build

echo "Ray $id has been installed."
