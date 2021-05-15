# Weather Lights

**Problem**: How might we represent weather information in a beautiful and intuitive display?

**Solution**: Display the weather on a colorful LED light strip using a raspberry pi connected to live weather info and forecasts

## Requirements
python 3.6.0 or above

## Reference
- Connecting raspberry pi to neopixels: https://learn.adafruit.com/neopixels-on-raspberry-pi
- CircuitPython LED Animations https://learn.adafruit.com/circuitpython-led-animations/
- SSH into Raspberry pi: https://www.raspberrypi.org/documentation/remote-access/ssh/
- OpenWeatherMap https://openweathermap.org/api/one-call-api --> pyowm https://pyowm.readthedocs.io/en/latest/
- Animation algorithm examples https://www.tweaking4all.com/hardware/arduino/adruino-led-strip-effects/

## Installation
#### Install dependencies
`sudo pip3 install -r requirements.txt`
`sudo python3 -m pip install --force-reinstall adafruit-blinka`

#### Set environment variables
1. get an OpenWeather API key from https://openweathermap.org/api
2. copy `.env.example` to `.env`: `cp .env.example .env`
3. update `OWM_API_KEY` in `.env` with your OpenWeather API key
4. set `WEATHERLIGHTS_LAT` and `WEATHERLIGHTS_LON` in `.env` to your latitude and longitude

#### Set up service
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
    (see https://www.raspberrypi.org/documentation/linux/usage/systemd.md for more info)

#### Mount Raspberry Pi as a Drive on PC
This allows you to use your code editor and edit files directly on the pi

PC:
1. Install sshfs:  https://github.com/billziss-gh/sshfs-win
2. Connect Raspberry pi:
- File Explorer > This PC > Map Network Drive
- Folder:     \\sshfs\pi@[your-pi-ip-here]
