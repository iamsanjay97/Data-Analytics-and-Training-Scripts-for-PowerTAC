#!/bin/bash

number_of_games=1

path="/mnt/d/PowerTAC/PowerTAC2021/server/server-distribution/finals_2019"

count=0

while [ $count -lt $number_of_games ]
do
    boot_file=$( shuf -n 1 available_boot_files.txt )

    echo "Game started with boot_file $boot_file"
    random_id=$((1 + $RANDOM % 10000))

    # mvn -Pcli -Dexec.args="--sim --boot-data $path/$boot_file.xml --weather-data $path/log/$boot_file.state --brokers VidyutVanika --game-id ${boot_file}_$random_id --log-suffix ${boot_file}_$random_id"
    mvn -Pcli -Dexec.args="--sim --boot-data $path/$boot_file.xml --weather-data $path/log/$boot_file.state --brokers VidyutVanika22 --game-id ${boot_file}_$random_id"

    count=$((count+1))

done

echo "Exeperiment Successfully Over !!!"
