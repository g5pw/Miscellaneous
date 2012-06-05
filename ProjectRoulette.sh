#!/usr/bin/env zsh -f
# vim: ft=zsh

case $1 in
	week )
		source=$(date +%W);;
	day )
		source=$(date +%d);;
	* )
		echo "Usage: $0 week|day"
		exit;;
esac

active=( $($HOME/.bin/openmeta -t -p $HOME/Documents/Projects/*(/) | fgrep active | sed 's/.* //') )
echo $( basename ${active[$(($source % ${#active[@]} +1))]} )
