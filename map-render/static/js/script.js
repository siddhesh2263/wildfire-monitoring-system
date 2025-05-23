let map = L.map('map').setView([31.6, -110.75], 11);

// Add satellite tile layer
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Esri World Imagery'
}).addTo(map);

let markers = [];

// Fetch and update map continuously
function fetchAndUpdate() {
    fetch("/data")
        .then(response => response.json())
        .then(data => {
            updateMap(data);
        });
}

function updateMap(dataPoints) {
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];

    let total = 0, high = 0, medium = 0, low = 0;

    dataPoints.forEach(point => {
        total++;
        if (point.intensity === "high") high++;
        else if (point.intensity === "medium") medium++;
        else low++;

        const marker = L.circleMarker([point.latitude, point.longitude], {
            radius: 6,
            color: getColor(point.intensity),
            fillOpacity: 0.7
        }).addTo(map);

        marker.bindPopup(
            `Lat: ${point.latitude}<br>
             Lon: ${point.longitude}<br>
             Time: ${point.timestamp}<br>
             Intensity: ${point.intensity}<br>
             Confidence: ${point.confidence_score}`
        );
        markers.push(marker);
    });

    // Update counts in UI
    document.getElementById("totalCount").textContent = `Total: ${total}`;
    document.getElementById("highCount").textContent = high;
    document.getElementById("mediumCount").textContent = medium;
    document.getElementById("lowCount").textContent = low;
}

function getColor(intensity) {
    switch (intensity) {
        case "high": return "red";
        case "medium": return "orange";
        default: return "yellow";
    }
}

// Refresh every 5 seconds
fetchAndUpdate();
setInterval(fetchAndUpdate, 5000);