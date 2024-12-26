#!/bin/bash

# Pooling interval in seconds, 4 seconds is the default as CO2 sensor works every 4 seconds
interval=4

watch -pbn$interval '

	# Human interface device identified by OS, might be different number
	device=/dev/$(sudo dmesg  | grep -i 'SLAB HT2000' | grep -o 'hidraw[0-9]\+' | head -1)

	logFileName=$(date +%Y-%m-%d).csv
	if [ $logFileName!=$oldLogFileName ]
	then
		if [ ! -f $logFileName ]
		then
			# First line of CSV file
			echo "time, timeStamp, internalTime, T, RH, CO2" > $logFileName
		fi
		oldLogFileName=$logFileName
	fi
	comandOutput=$(./ht2000 $device) &&
	echo $(date -Iseconds)", "$comandOutput | tee -a $logFileName
'
