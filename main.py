# Python Libraries
import argparse
import datetime
import json
import csv
import threading
import time
import adafruit_dht
import board
import numpy as np
import os
import I2C_LCD_driver
from astral import LocationInfo
from astral.sun import sun

# https://gist.github.com/elizabethn119/25be959d124f4b4c86f7160cf916f4d4

# Command line arguments
def get_args():
    parser = argparse.ArgumentParser(description='A Python Temperature sensor logger and web server')
    parser.add_argument("-c", "--config", dest="config_file", help="Location of the config file. Default: ./config.json", metavar="<path>",default="./config.json")
    return parser.parse_args()

def load_config(config_file):
    with open("./config.json") as config_file:
        d = json.load(config_file)
        config_file.close()
    return d

def create_csv(output_file):
    csv_file = open(output_file,"w")
    csv_file.write("Date/Time,Temperature(Outdoor),Humidity(Outdoor)(%),Temperature(Indoor),Humidity(Indoor)(%)\n")
    csv_file.close()

def log_to_csv(output_file,this_line):
    with open(output_file, 'a', newline='\n', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(this_line)

def read_log_temperature(timeout,metric_units):    
    dhtSensor1 = adafruit_dht.DHT22(board.D23)
    dhtSensor2 = adafruit_dht.DHT22(board.D24)

    while True:
        #current_time = datetime.now().strftime("%Y-%m-%d %H%M:%S")
        current_time = np.datetime64('now')

        global S1_humidity
        global S1_temperature

        # Sensor 1
        try:
            S1_humidity = dhtSensor1.humidity
            S1_temperature = dhtSensor1.temperature
        except RuntimeError:
            S1_humidity = None
            S1_temperature = None
        
        # Sensor 2
        try:
            S2_humidity = dhtSensor2.humidity
            S2_temperature = dhtSensor2.temperature
        except RuntimeError:
            S2_humidity = None
            S2_temperature = None

        # TESTING NUMBERS
        # temperature = round(random.uniform(-40.0,80.0),1)
        # humidity = round(random.uniform(0.0,100.0),1)


        #"Date/Time,Temperature(S1),Temperature(S2),Humidity(S1)(%),Humidity(S2)(%),Average_Temp,Average_Humidity
        log_to_csv("./Output.csv",[current_time,S1_temperature,S1_humidity,S2_temperature,S2_humidity])

        time.sleep(timeout)

def lcd_display():
    max_temp = 0
    max_humid = 0
    day = "not_set"

    global gpio_display
    gpio_display = I2C_LCD_driver.lcd()
    gpio_display.lcd_clear()
    while True:
        # if the day varaible no longer is the current day
        if day != time.strftime("%a"):
            # clear max values
            S1_max_temp = 0
            S1_max_humid = 0
            S2_max_temp = 0
            S2_max_humid = 0
            # collect dawn/dusk times
            city = LocationInfo("London", "England", "Europe/London", 51.5, -0.116)
            s = sun(city.observer)
            dawn = str(s["dawn"])
            dawn = ":".join(dawn.split(" ")[1].split(".")[0].split(":")[0:2])
            dusk = str(s["dusk"])
            dusk = ":".join(dusk.split(" ")[1].split(".")[0].split(":")[0:2])
            # make the day variable = today
            day = time.strftime("%a")

        s = f"{time.strftime('%H:%M')}     Indoor"
        s2 = f"{time.strftime('%H:%M')}    Outdoor"
        # Display Indoor Infomation
        gpio_display.lcd_display_string(f"{time.strftime('%H:%M')}     Indoor",line=1)

        if S1_temperature == None or S1_humidity == None:
            gpio_display.lcd_display_string("Runtime Error :( ",line=2)
        else:            
            gpio_display.lcd_display_string(str(S1_temperature)+"C      "+str(S1_humidity)+"%",line=2)
        time.sleep(5)

        if isinstance(S1_temperature, float) and isinstance(S1_humidity, float):
            if S1_temperature > S1_max_temp:
                S1_max_temp = S1_temperature
            if S1_humidity > S1_max_humid and isinstance(S1_humidity, float):
                S1_max_humid = S1_humidity
        if config["lcd_display"]["max_values"] == True:
            gpio_display.lcd_display_string("Max Temp:  "+str(S1_max_temp)+"C",line=2)
            time.sleep(5)
            gpio_display.lcd_display_string("Max Humid: "+str(S1_max_humid)+"%",line=2)
            time.sleep(5)
        

        if config["lcd_display"]["dawn_dusk"] == True:
            gpio_display.lcd_display_string("Dawn:      "+str(dawn),line=2)
            time.sleep(2)
            gpio_display.lcd_display_string("Dusk:      "+str(dusk),line=2)
            time.sleep(2)

if __name__ == "__main__":
    print("Raspberry Pi Temperature & Humidity Logger!")
    
    arguments = get_args()

    global config
    config = load_config(arguments.config_file)
    
    if os.path.exists("log.txt"):
        os.remove("log.txt")
    
    # if os.path.exists("Output.csv"):
    #     os.rename("./Output.csv",f"../Sample_Data/{datetime.now().strftime('%Y-%m-%dT%H%M:%S')}_Old.csv")

    create_csv(config["logging"]["CSV_output_path"])

    S1_temperature = 0
    S1_humidity = 0

    # Pass Temperature logging out to a new thread, can keep webserver running at same time! #multitasking
    temp_log_thread = threading.Thread(target=read_log_temperature, args=(5))
    display_thread = threading.Thread(target=lcd_display)
    temp_log_thread.start()
    display_thread.start()
