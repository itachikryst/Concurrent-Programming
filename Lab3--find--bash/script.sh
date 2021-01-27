#!/bin/bash

DIR_NAME=$1
FILE_NAME=$2
CHILD_PROCESS=$3
PROCESS_IDS=
COUNTER=0
SAVEIFS=IFS
IFS=$(echo -en "\n\b")

for SUBDIR in $(find "$DIR_NAME" -maxdepth 1 -mindepth 1 -type d) 
do
	bash $0 "$SUBDIR" "$FILE_NAME" "TRUE" & PROCESS_IDS+=("$!")
done

for FOUND_FILE in $(find "$DIR_NAME" -maxdepth 1 -mindepth 1 -type f -printf "%f\n") 
do
	if [ "$FOUND_FILE" == "$FILE_NAME" ]; then
		echo "Znaleziono '$FILE_NAME' w folderze '$DIR_NAME'"
		COUNTER=$((COUNTER+1))
	fi
done

for PROCESS_ID in "${PROCESS_IDS[@]}" 
do
	if [ "$PROCESS_ID" ]; then
	    wait "$PROCESS_ID"
	    COUNTER=$((COUNTER+$?))
	fi
done

if [ -z "$CHILD_PROCESS" ]; then
	if [ "$COUNTER" -eq 0 ]; then
	    echo "Nie znaleziono"
	fi
fi

IFS=$SAVEIFS
exit "$COUNTER"