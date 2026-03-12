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


var map = L.map('map').setView([20,78],4)

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
maxZoom:18
}).addTo(map)
