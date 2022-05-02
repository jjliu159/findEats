// global variable array
var array;
var markers = []

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 40.76, lng: -73.983 },
        zoom: 15,
        mapTypeId: "terrain",
    });

    map.setTilt(45);
    // var clickListener = google.maps.event.addListener(map, 'click', function(event) {
    //     new google.maps.Marker({
    //         position: event.latLng,
    //         map: map,
    //     });
    //     console.log(">>", event.latlng)
    //     console.log(event.latLng.toJSON())
    //     google.maps.event.removeListener(clickListener);
    // });

    // Initialize the GeoCode API
    const geocoder = new google.maps.Geocoder()

    // When user clicks submit-btn --> use geocode on the given address
    document.getElementById("submit-btn").addEventListener("click", () => {
      clearMarkers();
      geocodeAddress(geocoder, map);  
    });
    
}

function clearMarkers() {
  // delete markers from map after every search
  for (let i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
  // reset list of markers for map
  markers = []
}

function displayPins(data) {
    // var mapCanvas = document.getElementById('map_canvas');
    var location, marker;
    for (let i = 0; i < data.length; i++) {
        // location = new google.maps.LatLng(data[i]["latitude"],data[i]["longitude"]);
        new google.maps.Marker({
            position: { lat: data[i]["latitude"], lng: data[i]["longitude"] },
            map: map,
        });
        // marker = new google.maps.Marker({position:location});
        // marker.setMap(mapCanvas);
    }
}

function sendCoord(lat, lng) {
    var dict = {
        "Latitude": lat,
        "Longitude": lng,
    };
    $.post("/getPins", dict, function(data, status) {
        displayPins(JSON.parse(JSON.stringify(data)));
        array = JSON.parse(JSON.stringify(data))
        displayStores();
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
            const marker = new google.maps.Marker({
                map: inputMap,
                position: results[0].geometry.location,
            });

            // list of markers on the map
            markers.push(marker)

        } else {
            alert("Geocode error: " + status);
        }
    });
}

function decrementCount(id) {
  curIndex = 0
  
  //find the correct index manually since it's mismatched improperly
  for (let i = 0; i < array.length;i++){
      if (array[i]["id"] == id){
          curIndex = i;
      }
  }

  count = array[curIndex]["count"]
  $.post("/decrementCount", { "id": id, "count": count }, function(data, status) {
      if (status == "success") {
          count = document.getElementById(id).innerHTML;
          count = count.slice(15);
          document.getElementById(id).innerHTML = "Reserve Count: " + (parseInt(count) - 1);
          array[curIndex]["count"] -= 1;

          // confirmation message of reservation
          alert("You have made a reservation at " + array[curIndex]["restName"] + 
          ". Please provide your username and email upon arrival at " + array[curIndex]["restAddress"] + "."
          + " As well as this special code: " + array[curIndex]['code'])
          
          if (count <= "1") {
              displayStores(array);
          }
      }
  })

}

const displayStores = () => {
    let html = '';
    const table = document.getElementById("sidebar");
    array.forEach(({ id, count, restName, restAddress, description }) => {
        if (count > 0) {
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
        }

    })
    table.innerHTML = html;
}