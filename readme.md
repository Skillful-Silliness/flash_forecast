# Weather Lights

**Problem**: How might we represent weather information in a beautiful and intuitive display?

**Solution**: Display the weather on a colorful LED light strip using a raspberry pi connected to live weather info and forecasts

## Set-up

- Connecting raspberry pi to neopixels: https://learn.adafruit.com/neopixels-on-raspberry-pi
- SSH into Raspberry pi
- OpenWeatherMap https://openweathermap.org/api/one-call-api --> pyowm https://pyowm.readthedocs.io/en/latest/

## Installing
1. update lines 6-7 in lights.service to point to the correct script file where you have installed this
1. to create the service on raspberry pi and run it at startup:
    ```
    sudo cp myscript.service /etc/systemd/system/myscript.service
    sudo systemctl enable myscript.service
    ```
    (see https://www.raspberrypi.org/documentation/linux/usage/systemd.md for more info)
1. get an OpenWeather API key from https://openweathermap.org/api
1. copy `.env.example` to `.env` and update it with your API key
