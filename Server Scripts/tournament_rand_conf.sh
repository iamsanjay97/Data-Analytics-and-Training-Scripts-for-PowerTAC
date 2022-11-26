#!/bin/bash

number_of_games=1
number_of_opponents=0

path="/mnt/d/PowerTAC/PowerTAC2021/server/server-distribution/finals_2019"

broker_list=( "VidyutVanika21" "VV18" "AgentUDE" "CrocodileAgent" "TUC_TAC" "Sample" )

count=0

while [ $count -lt $number_of_games ]
do
    boot_file=$( shuf -n 1 available_boot_files.txt )

    echo "Game started with boot_file $boot_file"

    random_id=$((1 + $RANDOM % 10000))  

    current_brokers="VidyutVanika22,"
    for j in $( shuf -n $number_of_opponents --input-range=0-$((${#broker_list[@]}-1)) );
    do
        current_brokers+="${broker_list[j]},"
    done  
    echo "Participant brokers $current_brokers" 

    mvn -Pcli -Dexec.args="--sim --boot-data $path/$boot_file.xml --weather-data $path/log/$boot_file.state --brokers $current_brokers --game-id ${boot_file}_$random_id --config config/server.properties"

    count=$((count+1))
done

echo "Exeperiment Successfully Over !!!"
