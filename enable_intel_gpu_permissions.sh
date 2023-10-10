#!/bin/bash

GIDS=`stat -c "%g" /dev/dri/render*`
LAST_GID=
DOCKER_ADD_GROUPS=

for GID in $GIDS
do
	if [ "$LAST_GID" != "$GID" ] 
	then
		DOCKER_ADD_GROUPS="$ADD_GROUPS --group-add $GID"
		#echo "$DOCKER_ADD_GROUPS"		
		LAST_GID=$GID
	fi
done
