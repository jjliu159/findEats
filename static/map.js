
var map;
function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
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
      console.log(">>",event.latlng)
      console.log(event.latLng.toJSON())
      google.maps.event.removeListener(clickListener);
  });
  
  // Initialize the GeoCode API
  const geocoder = new google.maps.Geocoder()

  // When user clicks submit-btn --> use geocode on the given address
  document.getElementById("submit-btn").addEventListener("click", () => {geocodeAddress(geocoder, map);
  });
  
}

function displayPins(data){
  // var mapCanvas = document.getElementById('map_canvas');
  var location, marker;
  console.log(typeof(data));
  for (let i = 0; i < data.length; i++) {
    console.log({lat: data[i]["latitude"], lng: data[i]["longitude"]});
    console.log(map);
    // location = new google.maps.LatLng(data[i]["latitude"],data[i]["longitude"]);
    new google.maps.Marker({
      position: {lat: data[i]["latitude"], lng: data[i]["longitude"]},
      map: map,
    });
    // marker = new google.maps.Marker({position:location});
    // marker.setMap(mapCanvas);
  }
}

function sendCoord(lat, lng) {
  var dict = {"Latitude" : lat, 
                "Longitude" : lng,
              };
  $.post( "/getPins", dict,function(data, status){
    console.log("Data: " + data.longitude + "\nStatus: " + status);
    displayPins(JSON.parse(JSON.stringify(data)));
  })
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