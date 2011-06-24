if [ ! -d $1 ]; then
	echo "================================================"
	echo "                                              "
	echo "  Usage: $0 [directory to archive]  "
	echo "                                              "
	echo "================================================"
	exit -1
fi

PROJECT_DIR="$HOME/Documents/Projects"
ARCHIVE_DIR="Archive"
filename=`basename $1`
tags=`mdls -name kOMUserTags $1 | sed -e '1d' -e '$d' -e 's/^ *//g' -e 's/,//g'`
CATEGORY=""
echo $tags
for tag in $tags; do
	case $tag in
		"electronics" )
			CATEGORY="Electronics/"
			echo "Electronics stuff"
			;;
			
		"code" | "programming" )
			CATEGORY="Code/"
			echo "Coding stuff"
			;;
		"meta" )
			echo "Cannot archive meta folder. Exiting..."
			exit -1
			;;
		* )
			echo "Random stuff"
			;;
	esac
done
cd $PROJECT_DIR
zip -r $ARCHIVE_DIR/$CATEGORY$filename $filename > /dev/null #Archiving directory
if [ $? -ne 0 ]; then
	echo "An error ($?) occured during file zipping!"
	exit $?
fi

echo "Now I will delete the original directory."
echo -n "Do you want that? [Y/n] "
read ans
if [ $ans -a $ans = 'n' ]; then
	echo "Not deleting as requested"
else
	rm -rfv $filename
fi