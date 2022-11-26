#!/bin/bash

for i in {1..100000}
do
    # mvn test exec:exec -Dexec.args="--config broker.properties --jms-url tcp://host.name:61616 --repeat-count 100"
    mvn exec:exec
done