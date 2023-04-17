#!/bin/bash
cd /home/jibon/python/autometic-deploy/queue
./push.sh

./01.sh && mv 01.sh _01.sh
./push.sh

./02.sh && mv 02.sh _02.sh
./push.sh

./03.sh && mv 03.sh _03.sh
./push.sh

./04.sh && mv 04.sh _04.sh
./push.sh

./05.sh && mv 05.sh _05.sh
./push.sh