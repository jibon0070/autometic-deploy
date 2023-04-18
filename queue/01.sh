#!/bin/bash
cd /home/jibon/python/autometic-deploy

python scheduler.py --dev "2023-04-19 5:21 AM" -b "reseller-bill-monthly" -u "https://www.facebook.com/messages/t/5020246434759915/" "Messenger URI" -m "reseller account <cl>e <cl>bill <cl>masik kore diyechi." -p "Profile 2" "Browser Profile" -wd "~/website/media-online-billing" -wb "main" "Working Branch"