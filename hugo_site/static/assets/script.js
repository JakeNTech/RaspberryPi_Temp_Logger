function current_temp(){
    fetch("/api/current_temp")
    .then(function (response) {
        return response.text()
    }).then(function (text) {
        text = JSON.parse(text)
        document.getElementById("statistics").innerHTML = `<h2>Indoor</h2><p>Current Temperature: ${text["indoor"]["temp"]}C</p><p>Current Humidity: ${text["indoor"]["humidity"]}%</p><p>Maximum Temperature: ${text["indoor"]["max_temp"]}C</p><p>Maximum Humidity: ${text["indoor"]["max_humidity"]}%</p><h2>Outdoor</h2><p>Current Temperature: ${text["outdoor"]["temp"]}C</p><p>Current Humidity: ${text["outdoor"]["humidity"]}%</p><p>Maximum Temperature: ${text["outdoor"]["max_temp"]}C</p><p>Maximum Humidity: ${text["outdoor"]["max_humidity"]}%</p><h2>Pi</h2><p>Current Temperature: ${text["pi"]["cpu_temp"]}C</p><p>Current Utilistaion: ${text["pi"]["cpu_usage"]}%</p>`
    })
};

function current_temp_test(){
    document.getElementById("statistics").innerHTML = `<h2>Indoor</h2><p>Current Temperature: 34.8C C</p><p>Current Humidity: 55.5%</p><p>Maximum Temperature: 22.C</p><p>Maximum Humidity: 55.4%</p><h2>Outdoor</h2><p>Current Temperature:78.9C</p><p>Current Humidity: 02.36%</p><p>Maximum Temperature: 54.2C</p><p>Maximum Humidity: 55.2%</p>`
}

function get_statistics(){
    var parameters = `start_date=${document.getElementById("start_date").value}&end_date=${document.getElementById("end_date").value}`
    var url = "/api/get_stats?"+parameters
    fetch(url)
        .then(function (response) {
    return response.text();
        }).then(function (text) {
            text = JSON.parse(text)
            console.log(text)
            document.getElementById("stats_table").innerHTML=`<table><thead><tr><th></th><th>Indoor</th><th>Outdoor</th></tr></thead><tbody><tr><td>Max Temp</td><td>${text["Indoor"]["max_temp"]}C</td><td>${text["Outdoor"]["max_temp"]}C</td></tr><tr><td>Min Temp</td><td>${text["Indoor"]["min_temp"]}C</td><td>${text["Outdoor"]["min_temp"]}C</td></tr><tr><td>Max Humidity</td><td>${text["Indoor"]["max_humid"]}%</td><td>${text["Outdoor"]["max_humid"]}%</td></tr><tr><td>Min Humidity</td><td>${text["Indoor"]["min_humid"]}%</td><td>${text["Outdoor"]["min_humid"]}%</td></tr><tr><td>Average Temp</td><td>${text["Indoor"]["avg_temp"]}C</td><td>${text["Outdoor"]["avg_temp"]}C</td></tr><tr><td>Average Humidity</td><td>${text["Indoor"]["avg_humid"]}%</td><td>${text["Outdoor"]["avg_humid"]}%</td></tr></tbody></table>`
    })
}

function get_graphs(){
    fetch("/api/graph_maker")
        .then(function (response) {
    return response.text();
        }).then(function (text) {
            text = JSON.parse(text)
            document.getElementById("graph_display").innerHTML=`<img src="${text['temperature_graph']}"><img src="${text['humidity_graph']}"><img src="${text['CPUtemp_graph']}"><img src="${text['CPUusage_graph']}">`
    })
}