#!/bin/bash
cd /home/jibon/python/autometic-deploy

python scheduler.py -d "2023-05-02 07:56 PM" -b "verify-user" -u "https://www.facebook.com/messages/t/5020246434759915/" "Messenger URI" -m "user verify <cl>korar sisTem kore diyechi." -p "Profile 2" "Browser Profile" -wd "~/website/mymoviebazar.net" -wb "main" "Working Branch"
