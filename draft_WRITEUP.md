TICKER README

LICENSE:

    Copyright 2023, ROBERT HEETER

    Redistribution and use in source and binary forms, with or without 
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this 
    list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice, 
    this list of conditions and the following disclaimer in the documentation 
    and/or other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its contributors 
    may be used to endorse or promote products derived from this software without 
    specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

ABOUT:
    
    These scripts run the Ticker LED matrix on a PocketBeagle and includes several
    interactive widgets for the device.

SETUP:

    A. CHANGE FROM RPROC TO UIO via Cloud9 terminal
    
        cd /boot                            [to move to /boot directory]
        sudo nano uEnv.txt                  [to edit /boot/uEnv.txt]
        -                                   [make modifications; under PRU OPTIONS, comment out PRU RPROC line and uncomment PRU UIO line]
        ^X                                  ["ctrl+X" to exit editor]
        Y                                   ["Y" to save modified buffer]
        -                                   ["enter" to confirm file name]
        -                                   [shut off and restart the PocketBeagle to make PRU changes]

    B. CONNECT TO INTERNET via Cloud9 terminal
    
        Option 1. Using USB connection to a Mac computer:
    
        sudo dhclient usb1              [connect to internet using other computer]
        ping google.com                 [check internet connection]
        ^C                              ["ctrl+C" to quit checking internet connection]
    
        Option 2: Using USB connection to a Windows computer:
        
        /sbin/route add default gw 192.168.7.1
        echo "nameserver 8.8.8.8" >> /etc/resolv.conf
        
        Option 3. Using USB WiFi adapter:
    
        lsusb                           [to interact with USB WiFi adapter]
        sudo connmanctl                 [to modify WiFi connection]
            enable wifi                 [enables WiFi]
            scan wifi                   [scans for available networks]
            services                    [view available networks]
            agent on                    [turn on agent]
            connect [network ID]        [connect to network; use network ID not network name]
                                        [enter network password if required]
            services                    [check *AR or *AO next to network to indicate connected]
            quit                        [quit interface]
        ping google.com                 [check internet connection]
        ^C                              ["ctrl+C" to quit checking internet connection]

    C. IMPORTING PACKAGES via Cloud9 terminal
        
        sudo apt-get update
        sudo apt-get install python-pip -y
        sudo apt-get install python3-pip -y
        sudo apt-get install python3-pillow -y
        sudo apt-get install zip -y 
        sudo apt-get install libopenjp2-7 -y
        
        sudo pip3 install --upgrade Pillow
        sudo pip3 install --upgrade spotipy
        sudo pip3 install --upgrade Adafruit-Blinka
        sudo pip3 install --upgrade adafruit-circuitpython-ahtx0
    
    D. RUNNING TICKER ON BOOT via Cloud9 terminal
        
        cd /var/lib/cloud9                  [move to cloud9 folder]
        mkdir logs                          [make logs folder]
        sudo crontab -e                     [open crontab]
        -                                   [make modifications; add this line:
                                                @reboot sleep 60 && sh /var/lib/cloud9/projects/ticker/ticker_automatic.sh > /var/lib/cloud9/logs/cronlog 2>&1
                                            ]
        ^X                                  ["ctrl+X" to exit editor]
        Y                                   ["Y" to save modified buffer]
        -                                   ["enter" to confirm file name]
        -                                   [shut off and restart the PocketBeagle to make cron changes]

RUN:
    
    Restart the PocketBeagle before first run to ensure PRU changes have been set.
    Ensure the device is connected to a 5V/4A DC power source and the power switch
    has been set to "on".
    
    cd /var/lib/cloud9/projects/ticker  [to move to ticker directory]
    sudo python3 ticker.py              [to run ticker.py]
    -                                   [enter password, likely "temppwd"]
                                        
    On first run, paste the access token URL from spotify_setup.py when
    prompted in the Cloud9 terminal. This URL can only be used once (must
    regenerate a new one using spotify_setup.py if needed).

INSTRUCTIONS:
    
    A. GENERAL USE
    
        Cycle through widgets using the "<" and ">" buttons.
        Use the action button "•" on select widgets to perform actions.
        Adjust display brightness using the "+" and "-" buttons.
    
    B. WIDGET LIBRARY
    
        Widget
            Generic Widget class to display a white screen and supporting
            functions.
            
        ClockWidget
            ClockWidget class to display the current time and date.
            
        WeatherWidget
            WeatherWidget class to display the current temperature and humidity.
            
        SpotifyWidget
            SpotifyWidget class to display the currently playing track,
            pause/play, and skip to the next or previous track.
        
        See widget class files for additional documentation.
        