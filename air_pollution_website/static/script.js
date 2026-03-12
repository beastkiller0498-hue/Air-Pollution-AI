/* GRAPH */

const ctx = document.getElementById("pollutionChart")

new Chart(ctx,{
type:"bar",

data:{
labels:["PM2.5","PM10","NO2","SO2","O3"],

datasets:[{

label:"Pollution Levels",

data:[pm25,pm10,no2,so2,o3],

backgroundColor:[
"#ef4444",
"#f97316",
"#3b82f6",
"#22c55e",
"#6366f1"
]

}]
}

})



/* MAP */

var map=L.map('map').setView([20,78],5)

L.tileLayer(
'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
{
maxZoom:18
}).addTo(map)


/* MARKER */

var marker=L.marker([20,78]).addTo(map)

marker.bindPopup(`
<b>${city}</b><br>
AQI: ${aqi}
`)
.openPopup()



/* LEGEND */

var legend=L.control({position:"bottomright"})

legend.onAdd=function(){

var div=L.DomUtil.create("div","legend")

div.innerHTML+=
'<i style="background:#00e400"></i> Good <br>'

div.innerHTML+=
'<i style="background:#ffff00"></i> Fair <br>'

div.innerHTML+=
'<i style="background:#ff7e00"></i> Poor <br>'

div.innerHTML+=
'<i style="background:#ff0000"></i> Severe'

return div
}

legend.addTo(map)
