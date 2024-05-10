/*
Developed by Ellen Red
*/

document.addEventListener("DOMContentLoaded", function(event) {
    const getSensorReadings = function() {
        fetch('/update')
            .then((resp) => resp.json())
            .then(function(response) {
                document.getElementById('latitude').innerHTML =response.new_latitude;
                document.getElementById('longitude').innerHTML =response.new_longitude;
                document.getElementById('gps_time').innerHTML =response.new_gps_time;
                document.getElementById('satellites').innerHTML =response.new_satelites;
        });
    }

    getSensorReadings();
    setInterval(getSensorReadings, 100); 
});
