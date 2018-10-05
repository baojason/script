#!/bin/bash
ct=1
while [ $ct -lt 100 ];
do
    echo "<$1> Press [CTRL+C] to stop.."
    sleep 1
    let "ct++"
done
