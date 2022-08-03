# Python Libraries
import csv
import threading
import time
import subprocess

from requests import request
import adafruit_dht
import board
import numpy as np
# import os
import I2C_LCD_driver
from flask import Flask
from astral import LocationInfo
from astral.sun import sun
from data_utils import snazzy_data

# https://gist.github.com/elizabethn119/25be959d124f4b4c86f7160cf916f4d4

def create_csv(output_file):
    csv_file = open(output_file,"w")
    csv_file.write("Date/Time,Temperature(Outdoor),Humidity(Outdoor)(%),Temperature(Indoor),Humidity(Indoor)(%),RaspPi_Temp\n")
    csv_file.close()

def log_to_csv(output_file,this_line):
    with open(output_file, 'a', newline='\n', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(this_line)

def read_log_temperature():
    day = "not_set"
    outdoor_dhtSensor = adafruit_dht.DHT22(board.D23)
    indoor_dhtSensor2 = adafruit_dht.DHT22(board.D24)

    while True:
        #current_time = datetime.now().strftime("%Y-%m-%d %H%M:%S")
        current_time = np.datetime64('now')

        global outdoor_humidity
        global outdoor_temperature
        global indoor_humidity
        global indoor_temperature
        global outdoor_max_temp
        global outdoor_max_humid
        global indoor_max_temp
        global indoor_max_humid

        # Read from sensor
        try:
            outdoor_humidity = outdoor_dhtSensor.humidity
            outdoor_temperature = outdoor_dhtSensor.temperature
        except RuntimeError:
            outdoor_humidity = None
            outdoor_temperature = None
        
        try:
            indoor_humidity = indoor_dhtSensor2.humidity
            indoor_temperature = indoor_dhtSensor2.temperature
        except RuntimeError:
            indoor_humidity = None
            indoor_temperature = None

        # if the day variable no longer is the current day
        if day != time.strftime("%a"):
            # clear max values
            outdoor_max_temp = 0
            outdoor_max_humid = 0
            indoor_max_temp = 0
            indoor_max_humid = 0
            # make the day variable = today
            day = time.strftime("%a")
        
        # Compare new values to stored Max values for both sensors
        if isinstance(outdoor_temperature, float) and isinstance(outdoor_humidity, float):
            if outdoor_temperature > outdoor_max_temp:
                outdoor_max_temp = outdoor_temperature
            if outdoor_humidity > outdoor_max_humid and isinstance(outdoor_humidity, float):
                outdoor_max_humid = outdoor_humidity
        if isinstance(indoor_temperature, float) and isinstance(indoor_humidity, float):
            if indoor_temperature > indoor_max_temp:
                indoor_max_temp = indoor_temperature
            if indoor_humidity > indoor_max_humid and isinstance(outdoor_humidity, float):
                indoor_max_humid = indoor_humidity

        raspPi_temp = int(subprocess.run(['cat','/sys/class/thermal/thermal_zone0/temp'],stdout=subprocess.PIPE).stdout.decode('ascii'))/1000

        #"Date/Time,Temperature(outdoor),Temperature(indoor),Humidity(outdoor)(%),Humidity(indoor)(%),RaspPi_temp
        log_to_csv("./Output.csv",[current_time,outdoor_temperature,outdoor_humidity,indoor_temperature,indoor_humidity,raspPi_temp])

        time.sleep(5)

def lcd_display():
    # LCD Display Object
    gpio_display = I2C_LCD_driver.lcd()
    gpio_display.lcd_clear()

    while True:
        gpio_display.lcd_display_string(f"{time.strftime('%H:%M  %a %d/%m')}",line=1)

        if outdoor_temperature == None or outdoor_humidity == None or indoor_temperature == None or indoor_humidity == None:
            gpio_display.lcd_display_string("Runtime Error :( ",line=2)
        else:            
            gpio_display.lcd_display_string("In:  "+str(indoor_temperature)+"C "+str(indoor_humidity)+"%",line=2)
            time.sleep(5)
            gpio_display.lcd_display_string("Out: "+str(outdoor_temperature)+"C "+str(outdoor_humidity)+"%",line=2)
        
        time.sleep(5)

# Web Interface for better statistics
app = Flask(__name__)

#Send Index.html
@app.route('/')
def load_index():
    return app.send_static_file('index.html')
@app.route('/numbers/')
def load_stats():
    return app.send_static_file('numbers/index.html')
@app.route('/graphs/')
def load_graphs():
    return app.send_static_file('graphs/index.html')    

# Send Files to make index.html look nice and fancy
@app.route('/assets/JS/<file>')
def send_JS(file):
    asset_path = "assets/JS/"+file
    return app.send_static_file(asset_path)
@app.route('/sass/<file>')
def send_CSS(file):
    asset_path = "sass/"+file
    return app.send_static_file(asset_path)
# Send Graphs
@app.route('/assets/temp_storage/<file>')
def send_img(file):
    img_path = "assets/temp_storage/"+file
    return app.send_static_file(img_path)

# API actions
@app.route('/api/<action>',methods=['GET'])
def api_call(action):
    if action == "current_temp":
        json_response = {
            "indoor":{
                "temp":indoor_temperature,
                "humidity":indoor_humidity,
                "max_temp":indoor_max_temp,
                "max_humidity":indoor_max_humid
            },
            "outdoor":{
                "temp":outdoor_temperature,
                "humidity":outdoor_humidity,
                "max_temp":outdoor_max_temp,
                "max_humidity":outdoor_max_humid
            }
        }

    elif action == "dawn_dusk":
        #collect dawn/dusk times
        city = LocationInfo("London", "England", "Europe/London", 51.5, -0.116)
        s = sun(city.observer)
        dawn = str(s["dawn"])
        dawn = ":".join(dawn.split(" ")[1].split(".")[0].split(":")[0:2])
        dusk = str(s["dusk"])
        dusk = ":".join(dusk.split(" ")[1].split(".")[0].split(":")[0:2])
        json_response ={
            "dawn":dawn,
            "dusk":dusk
        }
    
    elif action == "temp_graph":
        snazzy_data.temp_humid_line_graph()
        json_response = {
            "temperature_graph":"/assets/temp_storage/temperature_LG.png",
            "humidity_graph":"/assets/temp_storage/humidity_LG.png",
        }

    return json_response

@app.route('/statistics',methods=['POST'])
def calc_stats():
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    json_response = snazzy_data.get_stats(start_date,end_date)
    return json_response

if __name__ == "__main__":
    print("Raspberry Pi Temperature & Humidity Logger!")
    
    # if os.path.exists("Output.csv"):
    #     os.rename("./Output.csv",f"../Sample_Data/{datetime.now().strftime('%Y-%m-%dT%H%M:%S')}_Old.csv")

    create_csv("./Output.csv")

    outdoor_temperature = 0
    outdoor_humidity = 0
    outdoor_temperature = 0
    outdoor_max_humid = 0
    indoor_temperature = 0
    indoor_humidity = 0
    indoor_max_temp = 0
    indoor_max_humid = 0

    # Pass Temperature logging out to a new thread, can keep webserver running at same time! #multitasking
    temp_log_thread = threading.Thread(target=read_log_temperature)
    display_thread = threading.Thread(target=lcd_display)
    temp_log_thread.start()
    display_thread.start()

    # Webserver for advanced statistics
    app.run(host="0.0.0.0")