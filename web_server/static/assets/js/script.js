function current_temp(){
    fetch("/api/current_temp")
    .then(function (response) {
        return response.text()
    }).then(function (text) {
        text = JSON.parse(text)
        console.log(text)
    })
};

function historic_temp(){
    fetch("/api/historic_temp")
    .then(function (response) {
        return response.text()
    }).then(function (text) {
        text = JSON.parse(text)
        console.log(text)
    })
};