# Python Libraries
import argparse
import json
import csv
import threading
from datetime import datetime
import time
import random
#import adafruit_dht

# My Libraries
from web_server import web_server

# https://gist.github.com/elizabethn119/25be959d124f4b4c86f7160cf916f4d4

# Command line arguments
def get_args():
    parser = argparse.ArgumentParser(description='A Python Temperature sensor logger and web server')
    parser.add_argument("-c", "--config", dest="config_file", help="Location of the config file. Default: ./config.json", metavar="<path>",default="./config.json")
    parser.add_argument("-w", "--webserver", dest="web_server", help="Run the Web server for a graphical output", action="store_true")
    return parser.parse_args()

def load_config(config_file):
    with open("./config.json") as config_file:
        d = json.load(config_file)
        config_file.close()
    return d

def error_logging(error_msg):
    log_for_logging = open("log.txt","a")
    log_for_logging.write(error_msg.strip()+"\n")
    log_for_logging.close()

def create_csv(output_file):
    csv_file = open(output_file,"w")
    csv_file.write("Date/Time,Temperature,Humidity(%)\n")
    csv_file.close()

def log_to_csv(output_file,this_line):
    with open(output_file, 'a', newline='\n', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(this_line)

def read_log_temperature(output_file,timeout,metric_units,max_readings):    
    # dhtSensor = adafruit_dht.DHT22(board.D4)

    reading_no = 0
    while reading_no < max_readings:
        # If first reading, skip timeout. Else: timeout
        if reading_no != 0:
            time.sleep(timeout)
        
        # try:
        #     humidity = dhtSensor.humidity
        #     temperature = dhtSensor.temperature
        # except Exception as error_msg:
        #     error_logging(error_msg)
        
        # TESTING NUMBERS
        temperature = round(random.uniform(-40.0,80.0),1)
        humidity = round(random.uniform(0.0,100.0),1)

        if metric_units == False:
            temperature = temperature * 9.0 / 5.0 + 32.0

        log_to_csv(output_file,[datetime.now().strftime("%d/%m/%YT%H:%M:%S"),temperature,humidity])

        reading_no = reading_no + 1
    
    print("Reached maximum read number! Stopping...")

if __name__ == "__main__":
    print("Raspberry Pi Temperature & Humidity Logger!")
    arguments = get_args()

    config = load_config(arguments.config_file)

    create_csv(config["file_paths"]["CSV_output_path"])

    # Pass Temperature logging out to a new thread, can keep webserver running at same time! #multitasking
    th = threading.Thread(target=read_log_temperature, args=(config["file_paths"]["CSV_output_path"],config["sensor"]["read_timeout"],config["sensor"]["metric_units"],config["sensor"]["max_readings"]))
    th.start()

    if arguments.web_server:
        web_server.web_runner(config["file_paths"]["CSV_output_path"])