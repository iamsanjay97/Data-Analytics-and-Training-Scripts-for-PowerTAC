#!/bin/bash

number_of_games=${1}      # Save first argument in a variable  (number of games in a set)
shift                     # Shift all arguments to the left (original $1 gets lost)
broker_directory=${1}     # Save second (now first) argument in a variable  (name of test set)
shift                     # Shift all arguments to the left (original $2 gets lost)
number_of_brokers=${1}    # Save third (now first) argument in a variable (number of brokers in a game)
shift                     # Shift all arguments to the left (original $3 gets lost)
broker_list=(${@})        # Rebuild the array with rest of arguments  (set of brokers to choose from)

path="/mnt/d/PowerTAC/PowerTAC2021/server/server-distribution/finals_2019"
path2="/mnt/d/PowerTAC/PowerTAC2021/brokers/Binaries/$broker_directory"
path3="/mnt/d/PowerTAC/PowerTAC2021/experiments/basic/"
path4="/mnt/d/PowerTAC/PowerTAC2021/plotting/"

declare -a boot_files=( "finals_2019_07_1" "finals_2019_07_2" "finals_2019_07_3" "finals_2019_07_5" "finals_2019_07_6" "finals_2019_07_7" "finals_2019_07_8" "finals_2019_07_9" "finals_2019_07_10" ) 

count=0

while [ $count -lt $number_of_games ]
do
    boot_file=$( shuf -n 1 available_boot_files.txt )

    echo "Game started with boot_file $boot_file"
    random_id=$((1 + $RANDOM % 10000))

    current_brokers=""
    for j in $( shuf -n $number_of_brokers --input-range=0-$((${#broker_list[@]}-1)) ); 
    do 
        current_brokers+="${broker_list[j]},"
    done

    echo "Participant brokers $current_brokers"

    mvn -Pcli -Dexec.args="--sim --boot-data $path/$boot_file.xml --weather-data $path/log/$boot_file.state --brokers $current_brokers --game-id ${boot_file}_$random_id --log-suffix ${boot_file}_$random_id"

    count=$((count+1))
    
    if [ $count -eq $number_of_games ]
    then
       break
    fi

done

echo "Exeperiment Successfully Over !!!"

sleep 5            # sleep for 10 seconds

# Store data in appropriate way and delete redundant broker binaries
for broker in ${broker_list[@]}
do
    mv $path2/$broker/AccountingInformationFile.csv $path2/${broker_directory}_AccountingInformation_$broker.csv
    rm -rf $path2/$broker
done

echo "Data Stored in Appropriate Files !!!"

mv $path2 $path3

cd $path4
python3 accounting_info.py $broker_directory

pkill screen       # kill all the broker screens

# to select a boot_file randomly
# rand=$[$RANDOM % ${#boot_files[@]}]
