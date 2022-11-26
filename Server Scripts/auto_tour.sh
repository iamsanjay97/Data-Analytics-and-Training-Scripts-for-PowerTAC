#!/bin/bash

## Script to run a set of games with multiple brokers
## Pass number of games $n in a set you want to run,
## directory $test in which you want to store the results,
## number of brokers $m in a game, and
## list of brokers $brokers to choose from

## If you want to run all the games against same brokers,
## then pass $brokers such that len(brokers)==m
## else to choose random brokers in each game
## pass len(brokers)>m

##### Limitations
## 1. More suitable to play with fixed set of brokers 
## 2. This script will run all the game with same number of brokers,
##    Update needed If you want to decide game-size randomly 
## 3. If you want to keep one broker fix, and randomly select 
##    opponent brokers, then script needs to be changes

read n             # number of games per set
read test          # name of the folder containing brokers for the set
read m             # number of brokers in a games
read -a brokers    # list of brokers

broker_path="/mnt/d/PowerTAC/PowerTAC2021/brokers/Binaries"
mkdir $broker_path/$test

for broker in ${brokers[@]}
do
  echo "Start the Broker $broker"
  cp -r $broker_path/$broker $broker_path/$test/$broker
  cd $broker_path/$test/$broker
  screen -dS $broker -m bash -c "bash run.sh"
done

echo "Start the Server"
cd /mnt/d/PowerTAC/PowerTAC2021/server/server-distribution
bash tournament.sh $n $test $m ${brokers[@]}
