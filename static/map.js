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
    
  }
  