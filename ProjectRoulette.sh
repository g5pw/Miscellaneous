#!/usr/bin/env zsh -f
# vim: ft=zsh
for project in $HOME/Documents/Projects/*(/); do
    if [[ -n $($HOME/.bin/openmeta -t -p $project | grep active) ]]; then
            active=( $active $(echo $project) )
    fi
done
case $1 in
	week )
		source=$(date +%W);;
	day )
		source=$(date +%d);;
	* )
		echo "Usage: $0 week|day"
		exit;;
esac

numProjects=${#active[@]}
echo "Got $numProjects active projects." 1>&2
focusing=$(($source % $numProjects))
focusingName=`basename ${active[$focusing]}`
echo $focusingName
