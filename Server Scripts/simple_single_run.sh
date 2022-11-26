#!/bin/bash

number_of_games=1

count=0

while [ $count -lt $number_of_games ]
do
    echo "Game number: $count"
    random_id=$((1 + $RANDOM % 10000))

    mvn -Pcli -Dexec.args="--sim --boot-data finals_2021/finals_2021_7.xml --weather-data random_seed/powertac-sim-random-seed.state --brokers VidyutVanika,VV18 --config config/server.properties --game-id VV22_DR_$random_id"
    # mvn -Pcli -Dexec.args="--sim --boot-data finals_2021/finals_2021_7.xml --weather-data finals_2021/log/finals_2021_7.log  --brokers VidyutVanika22 --config config/server.properties"
    count=$((count+1))

done
