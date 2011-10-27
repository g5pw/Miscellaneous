#!/bin/bash
for project in $(find  ~/Documents/Projects/ -type dir -depth 1); do
	tags=`mdls -raw -name kOMUserTags $project | sed -e '1d' -e '$d' -e 's/^ *//g' -e 's/,//g' -e 's/"//g'`
	for tag in $tags; do
		if [[ $tag = 'active' ]]; then
			active=( ${active[@]-} $(echo $project) )
			break
		fi
	done
done
numProjects=${#active[@]}
weekNum=`date +%W`
focusing=`expr $weekNum % $numProjects`
focusingName=`basename ${active[$focusing]}`
echo Focusing on: $focusingName
