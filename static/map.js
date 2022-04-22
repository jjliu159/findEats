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

function sendCoord(lat, lng) {
  var dict = {"Latitude" : lat, 
                "Longitude" : lng,
              };

    // var request = new XMLHttpRequest();
    // request.open('POST', '/getPins', true);
    // request.send(dict);

  $.post( "/getPins", dict);
  console.log("DICTIONARY: ", dict)
  /*
  $.post( "/getPins", {
    coords: dict 
});*/
}

function geocodeAddress(geocoder, inputMap) {
  const address = document.getElementById("address").value;

  // Search for the address with the API
  geocoder.geocode({ address: address }, (results, status) => {
    if (status === google.maps.GeocoderStatus.OK) {
        var lat = results[0].geometry.location.lat();
        var lng = results[0].geometry.location.lng();
        // Display Longitude and Latitude
        console.log("LAT: ", lat)
        console.log("LAT: ", lng)

        sendCoord(lat, lng);

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