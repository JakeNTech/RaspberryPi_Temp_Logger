# RaspberryPi_Temp_Logger
Some code to log and predict temperatures.

## Usage
A `config.json` is used to store parameters about the script:
```json
{
    "logging":{
        "read_timeout":5, //Time between readings
        "metric_units":true, //Celcius or Farenheight
        "CSV_output_path":"./Output.csv" //Output location
    },
    "sensor_1":{
        "name":"S1", // Sensor name in the output CSV file -> If you want to have each sensor in a different location
        "wire_colour":"Green", //NOT USED -> So I can remember which sensor is which
        "GPIO_pin":11, //NOT USED -> So I can remember which sensor is which
        "D_pin":17 //NOT USED -> So I can remember which sensor is which
    },
    "sensor_2":{
        "name":"S2", // Sensor name in the output CSV file -> If you want to have each sensor in a different location
        "wire_colour":"Yellow", //NOT USED -> So I can remember which sensor is which
        "GPIO_pin":13,  //NOT USED -> So I can remember which sensor is which
        "D_pin":27  //NOT USED -> So I can remember which sensor is which
    }
}
```
Command line options can also be used, to load up a different config file <!-- and web server options-->:
```console
> python .\main.py -h
Raspberry Pi Temperature & Humidity Logger!
usage: main.py [-h] [-c <path>] [-w]

A Python Temperature sensor logger and web server

optional arguments:
  -h, --help            show this help message and exit
  -c <path>, --config <path>
                        Location of the config file. Default: ./config.json
  -w, --webserver       Run the Web server for a graphical output
```
## Notes
This is still very much under development and has yet to be tested with an actual sensor!\
My GPIO Configuration, see [GPIO Pin out](https://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/):

-   Sensor 1: GPIO Pin 11, D17, Green Wire
-   Sensor 2: GPIO Pin 13, D27, Yellow Wire

## To Do
-   Test with actual sensor
-   Build Web Server

## Setup
There are two components to the software setup, Python libaries and some other ones (A StackOverflow post said to install them to fix an error I had):
```bash
sudo apt install libgpiod2
sudo apt install libcblas-dev
sudo apt install libhdf5-dev
sudo apt install libhdf5-serial-dev
sudo apt install libatlas-base-dev
sudo apt install libjasper-dev 
sudo apt install libqtgui4 
sudo apt install libqt4-test
sudo apt install libopenjp2-7
```