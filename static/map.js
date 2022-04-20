function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 40.76, lng: -73.983 },
    zoom: 15,
    mapTypeId: "terrain",
  });

  map.setTilt(45);
  var clickListener = google.maps.event.addListener(map, 'click', function (event) {
      new google.maps.Marker({
          position: event.latLng,
          map: map,
      });
      console.log(event.latLng.toJSON())
      google.maps.event.removeListener(clickListener);
  });
  
  // Initialize the GeoCode API
  const geocoder = new google.maps.Geocoder()

  // When user clicks submit-btn --> use geocode on the given address
  document.getElementById("submit-btn").addEventListener("click", () => {geocodeAddress(geocoder, map);
  });
  
}

function geocodeAddress(geocoder, inputMap) {
  const address = document.getElementById("address").value;

  // Search for the address with the API
  geocoder.geocode({ address: address }, (results, status) => {
    if (status === "OK") {
        // Display results
        //console.log(results)
        console.log(results[0].geometry.location);

        // Set the location of the map obtained by the API
        inputMap.setCenter(results[0].geometry.location);

        // Add the marker with the obtained location
        new google.maps.Marker({
            map: inputMap,
            position: results[0].geometry.location,
        });
    } else {
        alert("Geocode error: " + status);
    }
});
}