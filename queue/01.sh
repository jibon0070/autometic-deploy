#!/bin/bash
cd /home/jibon/python/autometic-deploy

python scheduler.py -d "2023-05-24 07:58 PM" -b "fix-users-search" -u "https://www.facebook.com/messages/t/5020246434759915/" "Messenger URI" -m "user search <cl>Thik kore diyechi." -p "Profile 2" "Browser Profile" -wd "~/website/mymoviebazar.net" -wb "main" "Working Branch"
