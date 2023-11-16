# **TICKER: LED matrix widgets via WiFi with a PocketBeagle**
- By **[Robert Heeter](https://github.com/rcheeter)**.
- Project completed 14 November 2023 for the ENGI 301 Introduction to Practical Electrical Engineering (Fall 2023) course with Professor Erik Welsh at Rice University.
- Much of the prototyping for this device was done at the Oshman Engineering Design Kitchen at Rice University in Houston, Texas.

## **License**
Copyright 2023, Robert Heeter.

See LICENSE (GNU General Public License, version 3).

## **About**
**64x32 LED matrix with WiFi, a temp/humidity sensor, and buttons in a laser cut housing; Python widget software framework on a PocketBeagle.**

This is the repository of the software framework for this project and contains software installation, setup, and running instructions.

## **Hardware & Operation**
See this [Hackster.io project article](https://www.hackster.io/rcheeter/ticker-led-matrix-widgets-via-wifi-with-a-pocketbeagle-edd915) for the hardware design and additional information about this project.

## **Software**
### ***PocketBeagle Setup***
For more specific information about this setup process, view the [beagleboard.org documentation](https://docs.beagleboard.org/latest/boards/pocketbeagle/original/ch03.html).

1. The BeagleBone Debian OS was used for this project. This can be installed for the PocketBeagle by programming a microSD card using a program like [Balena Etcher](https://etcher.balena.io) with the image file `bone-debian-10.11-iot-armhf-2022-02-03-4gb.img.xz`, [downloadable from rcn-ee.com](https://rcn-ee.com/rootfs/bb.org/testing/2022-02-03/buster-iot/). This specific version was used for this project.

2. After downloading the Debian OS, the microSD card can be inserted into the PocketBeagle and it can be connected to a Mac or Windows computer via a micro USB cable. Navigate to 192.168.6.2 (Mac) or 192.168.7.2 (Windows) on a web browser like Google Chrome to open Cloud9, the IDE used in this project for interacting with the PocketBeagle. For troubleshooting this process, consult see [this article by Random Nerd Tutorials](https://randomnerdtutorials.com/cloud9-ide-on-the-beaglebone-black/) or [this article by Dummies](https://www.dummies.com/article/technology/computers/hardware/beaglebone/how-to-launch-the-cloud9-ide-on-your-beaglebone-144962/) for the BeagleBoneBlack (which also applies for the PocketBeagle).

3. Open a new terminal and install the following packages and Python libraries required for this project:

    - `sudo apt-get update`
    - `sudo apt-get install python-pip -y`
    - `sudo apt-get install python3-pip -y`
    - `sudo apt-get install python3-pillow -y`
    - `sudo apt-get install zip -y`
    - `sudo apt-get install libopenjp2-7 -y`
    - `sudo pip3 install --upgrade Pillow`
    - `sudo pip3 install --upgrade spotipy`
    - `sudo pip3 install --upgrade Adafruit-Blinka`
    - `sudo pip3 install --upgrade adafruit-circuitpython-ahtx0`

### ***Project Installation & Setup***
1. Download the entire [**ticker**](https://github.com/rcheeter/ticker/tree/main/ticker) folder in this repository and drag it into a new folder named `projects` in the Cloud9 file manager as `/var/lib/cloud9/projects/ticker/...`. This folder contains all the scripts required to run the TICKER LED matrix and several starting widgets. This should appear similar to [this screenshot](https://github.com/rcheeter/ticker/blob/main/docs/software/file_organization.png), though it will likely be missing the `.cache`, `__pycache__`, and `logs/cronlog` files/folders in the screenshot.

2. Change the programmable realtime unit (PRU) mode in the PocketBeagle from RPROC to UIO to run the LED matrix. This can be done via the Cloud9 terminal:

    1. `cd /boot` to move to the `/boot` directory.
    2. `sudo nano uEnv.txt` to edit `/boot/uEnv.txt`. The password for debian is likely `temppwd`.
    3. Make modifications; under PRU OPTIONS, *comment out* the **PRU RPROC** line and *uncomment* the **PRU UIO** line.
    4. `^X`, "ctrl+X" to exit the editor.
    5. `Y`, "Y" to save the modified buffer.
    6. "enter" to confirm the file name.
    7. Shut off and restart the PocketBeagle using the power button to set the PRU changes.

    This should look similar to [this screenshot](https://github.com/rcheeter/ticker/blob/main/docs/software/pru/modify_pru_1.png) and [this other screenshot](https://github.com/rcheeter/ticker/blob/main/docs/software/pru/modify_pru_2.png).

3. Connect the PocketBeagle to the internet via the Cloud9 terminal using one of the following 3 options; the USB WiFi adapter should be used to allow the device to use the internet without a secondary internet-connected computer, but the first two options can be used for testing.
    
    **Option 1: USB connection to a Mac computer.**
        
    1. Ensure the Mac computer is connected to the PocketBeagle and that Internet Sharing is on in System Preferences > Sharing. There are numerous resources available on the internet to troubleshoot this process. Then perform the following in the Cloud9 terminal:
    2. `sudo dhclient usb1` to connect to the internet using the Mac computer. The password for debian is likely `temppwd`.
    3. `ping google.com` to check the internet connection.
    4. `^C`, "ctrl+C" to quit checking the internet connection.

    **Option 2: USB connection to a Windows computer.**

    1. Ensure the Windows computer is connected to the PocketBeagle. There are numerous resources available on the internet to troubleshoot this process. Then perform the following in the Cloud9 terminal:
    2. `/sbin/route add default gw 192.168.7.1`
    3. `echo "nameserver 8.8.8.8" >> /etc/resolv.conf` to connect to the internet using the Windows computer.
    4. `ping google.com` to check the internet connection.
    5. `^C`, "ctrl+C" to quit checking the internet connection.

    **Option 3: USB WiFi adapter.**
    
    1. Ensure the WiFi adapter is connected to the PocketBeagle's USB1 pins as outlined in the hardware documentation, then run the following in the Cloud9 terminal. This should look similar to [this screenshot](https://github.com/rcheeter/ticker/blob/main/docs/software/wifi/connect_wifi.png).
    2. `lsusb` to interact with the USB WiFi adapter.
    3. `sudo connmanctl` to modify the WiFi connection. The password for debian is likely `temppwd`.
    4. `enable wifi` to enable WiFi.
    5. `scan wifi` to scan for available networks.
    6. `services` to view available networks and their network IDs.
    7. `agent on` to turn on the WiFi agent.
    8. `connect [network ID]` to connect to a network; use the network ID, not the network name.
    9. Enter the network password if required.
    10. `services` should show `*AR` or `*AO` next to a network to indicate a connection.
    11. `quit` to quit the interface.
    12. `ping google.com` to check the internet connection.
    13. `^C`, "ctrl+C" to quit checking the internet connection.
    14. When the PocketBeagle (and by extension the WiFi adapter) are powered on, it will automatically attempt to connect to the same network. This process can be repeated to change networks.

4. To run the TICKER application on boot, perform the following in the Cloud9 terminal. This should be done only after testing the software using the Cloud9 terminal (i.e., not on boot).

    1. `cd /var/lib/cloud9` to move to the `/cloud9` directory.
    2. `mkdir logs` to make a `logs` folder.
    3. `sudo crontab -e` to open crontab. The password for debian is likely `temppwd`.
    4. Make modifications; add this line: `@reboot sleep 60 && sh /var/lib/cloud9/projects/ticker/run.sh > /var/lib/cloud9/logs/cronlog 2>&1`. This should be the only non-comment line in the crontab file.
    5. `^X`, "ctrl+X" to exit the editor.
    6. `Y`, "Y" to save the modified buffer.
    7. "enter" to confirm the file name.
    8. Shut off and restart the PocketBeagle using the power button to set the cron changes and test the automatic boot.

### ***Running the Application***
Restart the PocketBeagle before the first run to ensure the PRU changes have been set. Ensure the device is connected to a 5V/4A DC power source and the power switch has been set to "on". Run the following in the Cloud9 terminal:
    
1. `cd /var/lib/cloud9/projects/ticker` to move to the `/ticker` directory.
2. `sudo python3 ticker.py` to run `ticker.py`. The password for debian is likely `temppwd`.
                                        
On the first run, the SpotifyWidget will likely require an access token URL to be pasted into the Cloud9 terminal to run the application. See the SpotifyWidget section below for more information on how to do this.

### ***Widgets***
See the widget class Python files for additional documentation.

#### Widget
Generic Widget class to display a white screen and supporting functions. This class contains some general LED matrix and graphics parameters, including the pixel dimensions of the matrix and fonts.

Each widget inherits from this Widget class. Accordingly, each Widget must have the following functions:
- `setup(self)`: sets up any required APIs and initializes some class variables
- `update(self, action_state)`: updates and returns a new screen image (as a PIL Image object); the `action_state` parameter is an integer in [0, 1, 2, 3] to indicate the number of times that the action button has been pressed (i.e., no press, single press, double press, triple press); this update function can include a set of conditions to handle this user input.

Each Widget should also have the following properties:
- `refresh_rate`: the refresh rate of the display (in Hz), implemented as a waiting period between updating the screen image
- `verbose`: toggles the printing of detailed information from the widget to the terminal for debugging; it is recommended to set this to `False` to improve performance when running the final application.
 
#### Clock Widget
ClockWidget class to display the current time and date. Inherits Widget. Requires an internet connection to use the `datetime` library. Updates once per second.

#### Weather Widget
WeatherWidget class to display the current temperature and humidity. Inherits Widget. Does not require an internet connection. Requires the `adafruit_ahtx0` library to use the I2C AHT10 temperature/humidity sensor. Updates once per minute.

#### Spotify Widget
SpotifyWidget class to display the currently playing track, pause/play, and skip to the next or previous track. Inherits Widget. Requires an internet connection to use the `spotipy` Spotify API library. Updates continuously.

To set up this widget, a Spotify account is required and another computer (i.e., a Mac or Windows). Perform the following:
1. On the other computer, install Spotipy using the terminal: `pip install spotipy --upgrade`
2. Download the [**spotify_setup.py**](https://github.com/rcheeter/ticker/blob/main/setup/spotify_setup.py) script in this repository under the **setup** folder.
3. Create a [Spotify developer account](https://developer.spotify.com) and go to the Dashboard. This should look similar to [this screenshot](https://github.com/rcheeter/ticker/blob/main/docs/software/spotify/spotify_setup_1.png).
4. Create a new app with a name, description, and redirect URI (recommended to use `https://localhost:8888/callback`). This should look similar to [this screenshot](https://github.com/rcheeter/ticker/blob/main/docs/software/spotify/spotify_setup_2.png) and [this other screenshot](https://github.com/rcheeter/ticker/blob/main/docs/software/spotify/spotify_setup_3.png).
5. Navigate to the Settings > Basic Information page in the new app. This should look similar to [this screenshot](https://github.com/rcheeter/ticker/blob/main/docs/software/spotify/spotify_setup_4.png) and [this other screenshot](https://github.com/rcheeter/ticker/blob/main/docs/software/spotify/spotify_setup_5.png). Copy and save the `Client ID`, `Client Secret`, and `Redirect URI`. Never share or publish this information publicly.
6. Open the **spotify_setup.py** script and add the `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, and `SPOTIFY_REDIRECT_URI` parameters from the new app.
7. Ensure the computer is connected to the internet, and run the modified **spotify_setup.py** script (i.e., with Visual Studio Code) in a terminal. This should open a webpage on the computer's default browser for Spotify user authorization for the new app to access a particular user's Spotify data. This should look similar to [this screenshot](https://github.com/rcheeter/ticker/blob/main/docs/software/spotify/spotify_setup_6.png). This process follows the OAuth 2.0 authorization framework.
8. The user should log in to their Spotify account and agree to the permissions. This will redirect the user to a blank page with a URL under the `SPOTIFY_REDIRECT_URI`. This should look similar to [this screenshot](https://github.com/rcheeter/ticker/blob/main/docs/software/spotify/spotify_setup_7.png). Copy the entire URL from the browser page and save it to be pasted into the PocketBeagle terminal when first running the TICKER application. **Do NOT paste the URL into the local computer terminal. This URL contains the access token required to run Spotipy for the SpotifyWidget and should NEVER be shared or published publicly.**
9. Paste the access token URL from **spotify_setup.py** when prompted in the Cloud9 terminal when first running the TICKER application. This should look similar to [this screenshot](https://github.com/rcheeter/ticker/blob/main/docs/software/spotify/spotify_setup_8.png). This URL can only be used once; a new URL must be regenerated using spotify_setup.py if needed. If the URL is pasted into the terminal, the access token will be saved in a `.cache` file in the current directory so the user does not need to repeatedly provide a new access token.
10. A user can rescind authorization for TICKER to access their data from their Spotify account settings page.

TODO: Add more here.

## **Acknowledgements**
- ["64x32 LED Matrix Programming" article by Big Mess 'o Wires](https://www.bigmessowires.com/2018/05/24/64-x-32-led-matrix-programming/)
- ["RGB LED Panel Driver Tutorial" article by Glen Atkins](https://bikerglen.com/projects/lighting/led-panel-1up/)
- ["LEDscape" code via GitHub by Keith Hendrickson](https://github.com/KeithHenrickson/LEDscape)
- ["PRU Cookbook" code via GitLab by BeagleBoard](https://git.beagleboard.org/beagleboard/pru-cookbook-code)
- [Spotify Web API documentation](https://developer.spotify.com/documentation/web-api)
- [Spotipy documentation](https://spotipy.readthedocs.io/en/2.22.1/)
- [Adafruit CircuitPython AHTX0 library](https://github.com/adafruit/Adafruit_CircuitPython_AHTx0)
- [Pillow documentation](https://pillow.readthedocs.io/en/stable/)
- Professor Erik Welsh and his ENGI 301 Introduction to Practical Electrical Engineering course materials
