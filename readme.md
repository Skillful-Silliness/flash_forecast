# Weather Lights

**Problem**: How might we represent weather information in a beautiful and intuitive display?

**Solution**: Display the weather on a colorful LED light strip using a raspberry pi connected to live weather info and forecasts

## Requirements
- python 3.6.0 or above
- Rapsberry Pi 3 or 4 (Pi zero lags on animations)
- WS2812B LEDs (5 volt strip)
- Power source 5 Amp ... calculate 60mA / pixel

## Reference
- Installing Rapsberry Pi OS on a MicroSD card: https://www.raspberrypi.com/software/
- Connecting Raspberry Pi to NeoPixels: https://learn.adafruit.com/neopixels-on-raspberry-pi
- CircuitPython LED Animations https://learn.adafruit.com/circuitpython-led-animations/
- SSH into Raspberry pi: https://www.raspberrypi.org/documentation/remote-access/ssh/
- OpenWeatherMap https://openweathermap.org/api/one-call-api --> pyowm https://pyowm.readthedocs.io/en/latest/
- Animation algorithm examples https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/
- Redis Quick Start https://redis.io/topics/quickstart
- Wiring diagram: https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring#raspberry-pi-wiring-with-level-shifting-chip-3006459-3

## Installation
#### Install redis
1. go to your home directory `cd`
1. download the latest redis distribution `wget http://download.redis.io/redis-stable.tar.gz`
1. extract `tar xvzf redis-stable.tar.gz`
1. go into the extracted directory `cd redis-stable`
1. compile redis `make`
1. install binaries to the correct direcories `sudo make install`
1. create directories for config and data
    ```
    sudo mkdir /etc/redis
    sudo mkdir /var/redis
    ```
1. copy the init script into the proper directory `sudo cp utils/redis_init_script /etc/init.d/redis_6379`
1. copy the config file into the proper directory `sudo cp redis.conf /etc/redis/6379.conf`
1. create a directory for data `sudo mkdir /var/redis/6379`
1. edit the conf file (use whatever editor you want in place of vim) `sudo vim /etc/redis/6379.conf`
    * Set daemonize to yes (by default it is set to no).
    * Set the logfile to /var/log/redis_6379.log
    * Set the dir to /var/redis/6379
1. add the new Redis init script to all the default runlevels `sudo update-rc.d redis_6379 defaults`
1. start the redis service `sudo /etc/init.d/redis_6379 start` (this will start on reboot from now on)

#### Clone the repository
1. go to the directory where you want to install the code (we have used `Documents` by default) `cd ~/Documents`
1. clone the repository `git clone https://github.com/steryereo/weatherlights.git`
1. cd into the repo folder `cd weatherlights`

#### Install dependencies
`sudo pip3 install -r requirements.txt`
`sudo python3 -m pip install --force-reinstall adafruit-blinka`

#### Set environment variables
1. get an OpenWeather API key from https://openweathermap.org/api
2. copy `.env.example` to `.env`: `cp .env.example .env`
3. update `OWM_API_KEY` in `.env` with your OpenWeather API key
4. set `WEATHERLIGHTS_LAT` and `WEATHERLIGHTS_LON` in `.env` to your latitude and longitude

#### Set up services
see https://www.raspberrypi.org/documentation/linux/usage/systemd.md for more info

##### Lights service
1. copy `lights.service.example` to `lights.service`: `cp lights.service.example lights.service`
2. update lines 6-7 in `lights.service` to point to the correct script file where you have installed this
3. to create the service on raspberry pi and set it to run at startup:
    ```
    sudo cp lights.service /etc/systemd/system/lights.service
    sudo systemctl enable lights.service
    ```
    you can also start and stop the service with
    ```
    sudo systemctl start lights.service
    ```
    and
    ```
    sudo systemctl stop lights.service
    ```
##### Web server service
1. copy example service file `cp weatherlights_web.service.example weatherlights_web.service`
2. update lines 6-7 in `weatherlights_web.service` to point to the correct script file where you have installed this
3. to create the service on raspberry pi and set it to run at startup:
    ```
    sudo cp weatherlights_web.service /etc/systemd/system/weatherlights_web.service
    sudo systemctl enable weatherlights_web.service
    ```
    you can also start and stop the service with
    ```
    sudo systemctl start weatherlights_web.service
    ```
    and
    ```
    sudo systemctl stop weatherlights_web.service
    ```

#### Mount Raspberry Pi as a Drive on PC
This allows you to use your code editor and edit files directly on the pi

PC:
1. Install sshfs:  https://github.com/billziss-gh/sshfs-win
2. Connect Raspberry pi:
- File Explorer > This PC > Map Network Drive
- Folder:     `\\sshfs\pi@[your-pi-ip-here]`
