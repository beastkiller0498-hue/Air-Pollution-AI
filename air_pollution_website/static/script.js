navigator.geolocation.getCurrentPosition(function(position){

let lat = position.coords.latitude;
let lon = position.coords.longitude;

fetch(`/get_aqi?lat=${lat}&lon=${lon}`)
.then(res => res.json())
.then(data => {

document.getElementById("aqi").innerText = data.aqi
document.getElementById("status").innerText = data.status

})

})