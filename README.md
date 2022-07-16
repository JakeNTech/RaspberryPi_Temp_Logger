# RaspberryPi_Temp_Logger
Some code to log and predict temperatures.

## Usage
A `config.json` is used to store parameters about the script:
```json
{
    "sensor":{
        "read_timeout":60,  //The timeout between readings in seconds
        "metric_units":true,    //If you want to use Imperial units set to False
        "max_readings":2   //The maximum number of readings to take (Mainly for testing)
    },
    "file_paths":{
        "CSV_output_path":"./Output.csv" //The output path of the CSV Log file
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

