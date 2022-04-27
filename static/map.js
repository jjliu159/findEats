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
    displayStores(JSON.parse(JSON.stringify(data)));
  })
}

function geocodeAddress(geocoder, inputMap) {
  const address = document.getElementById("user_input_autocomplete_address").value;

  // Search for the address with the API
  geocoder.geocode({ address: address }, (results, status) => {
    if (status === google.maps.GeocoderStatus.OK) {
        var lat = results[0].geometry.location.lat();
        var lng = results[0].geometry.location.lng();
        // Display Longitude and Latitude

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

function decrementCount(id){
  console.log("ID: ",id)
  var count;
  $.post( "/decrementCount", {"id":id},function(data, status){
    count=document.getElementById(id).innerHTML;
    count = count.slice(15);
    console.log(">",(count),(parseInt(count)-1),"<");
    document.getElementById(id).innerHTML = "Reserve Count: " + (parseInt(count)-1);
  })

}

const displayStores = (array) => {
  let html = '';
  const table = document.getElementById("sidebar");
  console.log(array);
  array.forEach(({ id, count,restName, restAddress, description}) => {
    const card = `
    <a href="#" class="list-group-item list-group-item-action">
    <div class="d-flex w-100 justify-content-between">
      <h5 class="mb-1">${restName}</h5>
    </div>

    <h6 class="mb-1">${restAddress}</h3>
    <p class="mb-1" >${description} </p>
    <p class="mb-1" id = ${id} >Reserve Count: ${count}</p>

    <button onclick=decrementCount(${id})>Reserve Now</button>
  </a>
    `;

    html += card
  })
  table.innerHTML = html;
}
