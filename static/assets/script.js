function current_temp(){
    fetch("/api/current_temp")
    .then(function (response) {
        return response.text()
    }).then(function (text) {
        text = JSON.parse(text)
        document.getElementById("dynamic_page").innerHTML = `<div id="center_box"><h2>Indoor Stats</h2><p>Current Temperature: ${text["indoor"]["temp"]}C</p><p>Current Humidity: ${text["indoor"]["humidity"]}%</p><p>Maximum Temperature: ${text["indoor"]["max_temp"]}C</p><p>Maximum Humidity: ${text["indoor"]["max_humidity"]}%</p><h2>Outdoor Stats</h2><p>Current Temperature: ${text["outdoor"]["temp"]}C</p><p>Current Humidity: ${text["outdoor"]["humidity"]}%</p><p>Maximum Temperature: ${text["outdoor"]["max_temp"]}C</p><p>Maximum Humidity: ${text["outdoor"]["max_humidity"]}%</p></div>`
    })
};