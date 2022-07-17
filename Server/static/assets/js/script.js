function current_temp(){
    fetch("/api/current_temp")
    .then(function (response) {
        return response.text()
    }).then(function (text) {
        text = JSON.parse(text)
        document.getElementById("dynamic_page").innerHTML="<div id='center_box'><p>Sensor 1 Temprature: "+text["sensor_1"]["temp"]+"C</p><p>Sensor 2 Tempearature: "+text["sensor_2"]["temp"]+"C</p><p>Sensor 1 Humidity: "+text["sensor_1"]["humidity"]+"%</p><p>Sensor 2 Humidity: "+text["sensor_2"]["humidity"]+"%</p><p>Average Temprature: "+text["average"]["temp"]+"C</p><p>Average Humidity: "+text["average"]["humidity"]+"%</p></div>"
    })
};
