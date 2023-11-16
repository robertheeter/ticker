#!/bin/bash

# Run /projects/ticker/ticker.py automatically on boot with cron.
# See documentation at https://github.com/rcheeter/ticker for setting up cron.

cd /var/lib/cloud9/projects/ticker
sudo python3 ticker.py
