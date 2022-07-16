from flask import Flask, jsonify, request
import csv
import os

# Flask Functions
## https://github.com/JakeNTech/Bingo_WebServer/blob/main/main.py
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
# @app.route('/assets/img/<file>')
# def send_img(file):
#     img_path = "assets/img/"+file
#     return app.send_static_file(img_path)

@app.route('/api/<action>',methods=['GET'])
def api_call(action):
    if action == "current_temp":
        return(jsonify("Hello"))
    elif action == "historic_temp":
        return(jsonify(read_csv(csv_output_location)))

# Python Functions
def web_runner(csv_output_file):
    global csv_output_location
    csv_output_location = csv_output_file

    #app.run(host="0.0.0.0")
    app.run()

def read_csv(csv_file):
    loaded_csv = []
    with open(csv_file,newline="\n") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",", quotechar='|')
        for row in spamreader:
            loaded_csv.append(row)
    return loaded_csv

if __name__ == "__main__":
    app.run()
    
    global csv_output_location
    csv_output_location = "../Output.csv"
