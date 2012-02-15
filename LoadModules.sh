
# this script try to find a sutiable driver
# a driver just loads modules and sets paths

directory=$(echo ${BASH_SOURCE[0]}|sed 's=LoadModules.sh==g')

for driver in $(ls $directory/Drivers)
do
	source $directory/Drivers/$driver
done
