# Python Libraries
import argparse
import json
import csv
import threading
import time
from flask import Flask, jsonify, request
import adafruit_dht
import board
import numpy as np
import os

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
    log_for_logging.write(error_msg+"\n")
    log_for_logging.close()

def create_csv(output_file):
    csv_file = open(output_file,"w")
    csv_file.write("Date/Time,Temperature("+config["sensor_1"]["name"]+"),Temperature("+config["sensor_2"]["name"]+"),Humidity("+config["sensor_1"]["name"]+")(%),Humidity("+config["sensor_2"]["name"]+")(%),Average_Temp,Average_Humidity\n")
    csv_file.close()

def log_to_csv(output_file,this_line):
    with open(output_file, 'a', newline='\n', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(this_line)

def read_log_temperature(timeout,metric_units):    
    dhtSensor1 = adafruit_dht.DHT22(board.D17)
    dhtSensor2 = adafruit_dht.DHT22(board.D27)

    global S1_humidity
    global S1_temperature
    global S2_humidity
    global S2_temperature
    global temperature_avg
    global humidity_avg

    reading_no = 0
    while True:
        
        #current_time = datetime.now().strftime("%Y-%m-%d %H%M:%S")
        current_time = np.datetime64('now')
        # Sensor 1
        try:
            S1_humidity = dhtSensor1.humidity
            S1_temperature = dhtSensor1.temperature
        except RuntimeError:
            error = f"{current_time},Run Time Error, Sensor 1"
            error_logging(error)
            S1_humidity = None
            S1_temperature = None
        
        # Sensor 2
        try:
            S2_humidity = dhtSensor2.humidity
            S2_temperature = dhtSensor2.temperature
        except RuntimeError as error_msg:
            error = f"{current_time},Run Time Error, Sensor 2"
            error_logging(error)
            S2_humidity = None
            S2_temperature = None

        # TESTING NUMBERS
        # temperature = round(random.uniform(-40.0,80.0),1)
        # humidity = round(random.uniform(0.0,100.0),1)

        if metric_units == False:
            S1_temperature = S1_temperature * 9.0 / 5.0 + 32.0
            S2_temperature = S2_temperature * 9.0 / 5.0 + 32.0

        # If both sensors fail
        if S1_temperature == None and S2_temperature == None:
            print("Both sensors reading failed...Skipping..")
            error_logging(f"{current_time},Both Sensor reading failed,")
            temperature_avg = None
            humidity_avg = None
        # If sensor 1 failed -> Make Sensor 2 the Average
        elif S1_temperature == None and S1_humidity == None:
            temperature_avg = S2_temperature
            humidity_avg = S2_humidity
        # If sensor 2 failed -> Make Sensor 1 the Average
        elif S2_temperature == None and S2_humidity == None:
            temperature_avg = S1_temperature
            humidity_avg = S1_humidity
        # Otherwise Calculate the average between the two
        else:
            temperature_avg = round((S1_temperature+S2_temperature)/2,2)
            humidity_avg = round((S1_humidity+S2_humidity)/2,2)
        
        #"Date/Time,Temperature(S1),Temperature(S2),Humidity(S1)(%),Humidity(S2)(%),Average_Temp,Average_Humidity
        log_to_csv(config["logging"]["CSV_output_path"],[current_time,S1_temperature,S2_temperature,S1_humidity,S2_humidity,temperature_avg,humidity_avg])

        time.sleep(timeout)
    
# Web server, appeares to need to be in the same script for the global variables to work... I dunno either lol
app = Flask(__name__)

#Send Index.html
@app.route('/')
def load_index():
    return app.send_static_file('index.html')

# Send Files to make index.html look nice and fancy
@app.route('/assets/js/<file>')
def send_js(file):
    js_path = "assets/js/"+file
    return app.send_static_file(js_path)
@app.route('/assets/css/<file>')
def send_css(file):
    css_path = "assets/css/"+file
    return app.send_static_file(css_path)
@app.route('/assets/temp_storage/<file>')
def send_img(file):
    img_path = "assets/temp_storage/"+file
    return app.send_static_file(img_path)

# API actions
@app.route('/api/<action>',methods=['GET'])
def api_call(action):
    if action == "current_temp":
        json_responce = {
            "sensor_1":{
                "temp":S1_temperature,
                "humidity":S1_humidity,
            },
            "sensor_2":{
                "temp":S1_temperature,
                "humidity":S1_humidity,
            },
            "average":{
                "temp":temperature_avg,
                "humidity":humidity_avg
            }
        }
        return(json_responce)
    elif action == "historic_temp":
        return(jsonify(read_csv(config["logging"]["CSV_output_path"])))
    elif action == "download_csv":
        return(app.send_static_file(config["logging"]["CSV_output_path"]))

# Python Functions
def web_runner(csv_output_file):

    app.run(host="0.0.0.0")
    #app.run()

def read_csv(csv_file):
    loaded_csv = []
    with open(csv_file,newline="\n") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",", quotechar='|')
        for row in spamreader:
            loaded_csv.append(row)
    return loaded_csv

if __name__ == "__main__":
    print("Raspberry Pi Temperature & Humidity Logger!")
    arguments = get_args()

    S1_humidity = 0
    S1_temperature = 0
    S2_humidity = 0
    S2_temperature = 0
    temperature_avg = 0
    humidity_avg = 0

    global config
    config = load_config(arguments.config_file)
    
    if os.path.exists("log.txt"):
        os.remove("log.txt")
    
    if os.path.exists("Output.csv"):
        os.rename("./Output.csv",f"../Sample_Data/{np.datetime64('now')}_Old.csv")

    create_csv(config["logging"]["CSV_output_path"])

    # Pass Temperature logging out to a new thread, can keep webserver running at same time! #multitasking
    th = threading.Thread(target=read_log_temperature, args=(config["logging"]["read_timeout"],config["logging"]["metric_units"]))
    th.start()

    if arguments.web_server:
        web_runner(config["logging"]["CSV_output_path"])
