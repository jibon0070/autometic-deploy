#!/bin/bash
cd /home/jibon/python/autometic-deploy

python scheduler.py -d "Schedule Date" -b "To be merged branch" -u "https://www.facebook.com/messages/t/5020246434759915/" "Messenger URI" -m "Message" -p "Profile 2" "Browser Profile" -wd "Working Directory" -wb "main" "Working Branch"