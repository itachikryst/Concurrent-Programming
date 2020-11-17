#!/bin/bash
touch user_data
while inotifywait -q -e modify user_data >/dev/null; do
    typeset -i input=$(sed -n -e '$p' user_data)
    result=$(expr $input '*' $input)
		touch results
    echo $result >> results   
		> user_data
done