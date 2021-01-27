#!/bin/bash
PIDS=`pidof bash`
PIDS_ARR=($PIDS)
for pid in "${PIDS_ARR[@]:1}"
do
	if [ "$!" != "$pid" ]; then
		kill -SIGUSR1 $pid
	fi
done

trap "" SIGHUP SIGTERM SIGCHLD
trap "exit 0" SIGUSR1
SERVERQUEUE_FILEPATH="$HOME/serwerfifo"

function INPUT_TO_CLIENTQUEUE_FILEPATH {
    echo $(($2+10)) > $1
}

if [ -e $SERVERQUEUE_FILEPATH ]; then
    rm $SERVERQUEUE_FILEPATH
fi

mkfifo $SERVERQUEUE_FILEPATH
chmod 777 $SERVERQUEUE_FILEPATH

while true; do
    if read CLIENT_ARGUMENTS < $SERVERQUEUE_FILEPATH; then
        ARGUMENT_ARRAY=($CLIENT_ARGUMENTS)
        INPUT_TO_CLIENTQUEUE_FILEPATH ${ARGUMENT_ARRAY[0]} ${ARGUMENT_ARRAY[1]} &
    fi
done
