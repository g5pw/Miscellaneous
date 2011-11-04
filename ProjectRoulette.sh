#!/bin/bash
for project in $(find  ~/Documents/Projects/ -type dir -depth 1); do
    temp=`mdls -raw -name kOMUserTags $project | grep 'active'`
    if [[ -n $temp ]]; then
            active=( ${active[@]-} $(echo $project) )
    fi
done
numProjects=${#active[@]}
weekNum=`date +%W`
focusing=`expr $weekNum % $numProjects`
focusingName=`basename ${active[$focusing]}`
echo Focusing on: $focusingName
