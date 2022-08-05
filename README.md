# RaspberryPi_Temp_Logger
A clock with some extra functionality.

## GPIO Pinout
This is still very much under development and has yet to be tested with an actual sensor!\
My GPIO Configuration, see [GPIO Pin out](https://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/):

-   Sensor 1: GPIO Pin 16, D23, Outdoor
-   Sensor 2: GPIO Pin 18, D24, Indoor
-   LCD Display: GPIO Pins 03 05
-   Maplin 60mm Fan: GPIO Pin 02

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
pip3 install -r requirements.txt
```
## To Do
- Make Graphs and statistics work with Python

## To Build Hugo site
```console
rm -r ./static && cd ./hugo_site && hugo -d ../static --disableKinds=taxonomyTerm && cd ..
```