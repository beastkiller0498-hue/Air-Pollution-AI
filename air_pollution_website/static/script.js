/* MAP */

var lat = 17.0
var lon = 79.5

var map = L.map('map').setView([lat, lon], 5)

/* Base map */
L.tileLayer(
"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
{
maxZoom:18
}).addTo(map)


/* AQI Heatmap from OpenWeather */
L.tileLayer(
"https://tile.openweathermap.org/map/aqi/{z}/{x}/{y}.png?appid=YOUR_API_KEY",
{
opacity:0.6
}).addTo(map)


/* Marker */
var marker = L.marker([lat, lon]).addTo(map)

marker.bindPopup(`
<b>${city}</b><br>
AQI: ${aqi} - ${status}
`).openPopup()


/* -------- AQI LEGEND -------- */

var legend = L.control({position: "bottomright"})

legend.onAdd = function () {

var div = L.DomUtil.create("div", "legend")

div.innerHTML += "<h4>AQI Levels</h4>"

div.innerHTML +=
'<i style="background:#00e400"></i> Good <br>'

div.innerHTML +=
'<i style="background:#ffff00"></i> Fair <br>'

div.innerHTML +=
'<i style="background:#ff7e00"></i> Poor <br>'

div.innerHTML +=
'<i style="background:#ff0000"></i> Severe'

return div
}

legend.addTo(map)
