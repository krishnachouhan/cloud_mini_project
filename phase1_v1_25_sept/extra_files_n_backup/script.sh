#!/bin/sh
sudo apt-get install python-flask 
if [ "$#" -eq 3 ]; then 
	python ../src/routes.py "$@" 
else 
	echo "Invalid number of arguments !" 
fi
