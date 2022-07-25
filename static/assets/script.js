function current_temp(){
    fetch("/api/current_temp")
    .then(function (response) {
        return response.text()
    }).then(function (text) {
        text = JSON.parse(text)
        document.getElementById("dynamic_page").innerHTML = ```
            <div id="center_box">
            <h2>Indoor Stats</h2>
                <p>Current Temperature: ${response["indoor"]["temp"]}C</p>
                <p>Current Humidity: ${response["indoor"]["humidity"]}%</p>
                <p>Maximum Temperature: ${response["indoor"]["max_temp"]}C</p>
                <p>Maximum Humidity: ${response["indoor"]["max_humidity"]}%</p>
            <h2>Outdoor Stats</h2>
                <p>Current Temperature: ${response["outdoor"]["temp"]}C</p>
                <p>Current Humidity: ${response["outdoor"]["humidity"]}%</p>
                <p>Maximum Temperature: ${response["outdoor"]["max_temp"]}C</p>
                <p>Maximum Humidity: ${response["outdoor"]["max_humidity"]}%</p>
            </div>
        ```
    })
};