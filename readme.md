# Weather Lights

**Problem**: How might we represent weather information in a beautiful and intuitive display?

**Solution**: Display the weather on a colorful LED light strip using a raspberry pi connected to live weather info and forecasts

## Requirements
python 3.6.0 or above

## Set-up

- Connecting raspberry pi to neopixels: https://learn.adafruit.com/neopixels-on-raspberry-pi
- SSH into Raspberry pi: https://www.raspberrypi.org/documentation/remote-access/ssh/
- OpenWeatherMap https://openweathermap.org/api/one-call-api --> pyowm https://pyowm.readthedocs.io/en/latest/

## Installation
#### Install dependencies
`sudo pip3 install -r requirements.txt`
`sudo python3 -m pip install --force-reinstall adafruit-blinka`

#### Set up OpenWeather API credentials
1. get an OpenWeather API key from https://openweathermap.org/api
1. copy `.env.example` to `.env` and update it with your API key

#### Set up service
1. update lines 6-7 in lights.service to point to the correct script file where you have installed this
1. to create the service on raspberry pi and set it to run at startup:
    ```
    sudo cp myscript.service /etc/systemd/system/myscript.service
    sudo systemctl enable myscript.service
    ```
    you can also start and stop the service with
    ```
    sudo systemctl start lights.service
    ```
    and
    ```
    sudo systemctl stop myscript.service
    ```
    (see https://www.raspberrypi.org/documentation/linux/usage/systemd.md for more info)
