#!/bin/bash

# Run /projects/ticker/ticker.py automatically on boot with cron as follows:

# cd /var/lib/cloud9                  [move to cloud9 folder]
# mkdir logs                          [make logs folder]
# sudo chmod 777 /var/lib/cloud9/logs [modify permissions for logs folder]
# sudo crontab -e                     [open crontab]
# -                                   [make modifications; add this line:
#                                         @reboot sleep 60 && sh /var/lib/cloud9/projects/ticker/run.sh > /var/lib/cloud9/logs/cronlog 2>&1
#                                     ]
# ^X                                  ["ctrl+X" to exit editor]
# Y                                   ["Y" to save modified buffer]
# -                                   ["enter" to confirm file name]
# -                                   [shut off and restart the PocketBeagle to make cron changes]

cd /var/lib/cloud9/projects/ticker
sudo python3 ticker.py
