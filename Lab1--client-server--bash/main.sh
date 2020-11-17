#!/bin/bash
touch user_data
touch results
read -p "Enter a number to square: " input
echo $input >> user_data
while inotifywait -q -e modify results >/dev/null; do
    typeset -i result=$(sed -n -e '$p' results)
    echo "Your number squared is: "$result
		rm results
    break
done