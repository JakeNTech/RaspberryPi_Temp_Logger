function current_temp(){
    fetch("/api/current_temp")
    .then(function (response) {
        return response.text()
    }).then(function (text) {
        text = JSON.parse(text)
        document.getElementById("statistics").innerHTML = `<h2>Indoor</h2><p>Current Temperature: ${text["indoor"]["temp"]}C</p><p>Current Humidity: ${text["indoor"]["humidity"]}%</p><p>Maximum Temperature: ${text["indoor"]["max_temp"]}C</p><p>Maximum Humidity: ${text["indoor"]["max_humidity"]}%</p><h2>Outdoor</h2><p>Current Temperature: ${text["outdoor"]["temp"]}C</p><p>Current Humidity: ${text["outdoor"]["humidity"]}%</p><p>Maximum Temperature: ${text["outdoor"]["max_temp"]}C</p><p>Maximum Humidity: ${text["outdoor"]["max_humidity"]}%</p>`
    })
};

function current_temp_test(){
    document.getElementById("statistics").innerHTML = `<h2>Indoor</h2><p>Current Temperature: 34.8C C</p><p>Current Humidity: 55.5%</p><p>Maximum Temperature: 22.C</p><p>Maximum Humidity: 55.4%</p><h2>Outdoor</h2><p>Current Temperature:78.9C</p><p>Current Humidity: 02.36%</p><p>Maximum Temperature: 54.2C</p><p>Maximum Humidity: 55.2%</p>`
}