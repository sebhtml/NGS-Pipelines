#!/bin/bash

root=/mnt/scratch_mp2/corbeil/corbeil_group/
source $root/software/NGS-Pipelines/LoadModules.sh

cd ~/git-clones/ray

id=$(git log|grep ^commit|head -n1|awk '{print $2}')
builds=$root/software/RayAppBuilds/

make clean

make ASSERT=n DEBUG=n HAVE_LIBZ=y HAVE_LIBBZ2=y EXTRA=-march=native J=10 PREFIX=$builds/$id
make install

cd $builds
rm last-build
ln -s $id last-build
cd last-build
strip Ray

cd ~/git-clones/ray

echo "Ray $id has been installed."


