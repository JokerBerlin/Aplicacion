window.onload = function() {
    coordenadas.forEach(element => {
        // console.log(element);
        pos = {
            lat: parseFloat(element.lat),
            lng: parseFloat(element.lng)
        };

        config = {
            position: pos
        };

        addMarker(config)
    });

    var coords = Array();

    for (let i = 0; i < markers.length; i++) {
        const marker = markers[i];
        const coord = {lat: marker.position.lat(), lng: marker.position.lng()};
        coords.push(coord);
    }

    var waypts = Array();
    if (markers.length > 2) {
        for (let i = 1; i < markers.length - 1; i++) {
            waypts.push({
                location: markers[i].position,
                stopover: true
            })
        }
    } else {
        waypts = []
    }
    const origen = markers[0].position;
    const destino = markers[markers.length - 1].position;

    if (waypts.length > 0) {
        ds.route({
            origin: origen,
            destination: destino,
            waypoints: waypts,
            optimizeWaypoints: true,
            travelMode: 'DRIVING',
        }, function(response, status) {
            if (status === 'OK') {
                dr.setDirections(response);
            } else {
                alert('Error' + status);
            }
        })
    } else {
        ds.route({
            origin: origen,
            destination: destino,
            optimizeWaypoints: true,
            travelMode: 'DRIVING',
        }, function(response, status) {
            if (status === 'OK') {
                dr.setDirections(response);
            } else {
                alert('Error' + status);
            }
        })
    }

}

function addMarker(config) {
  var marker = new google.maps.Marker({
    position: config.position,
    map: mapa,
    draggable: false
  });
  markers.push(marker)
}

function initMap() {
  mapa = new google.maps.Map(document.getElementById('mapa'), {
    center: {lat: -13.1587800, lng: -74.2232100},
    zoom: 17
  });

  infoWindow = new google.maps.InfoWindow;

  ds = new google.maps.DirectionsService();
  dr = new google.maps.DirectionsRenderer({map: mapa, suppressMarkers: true});

  // Try HTML5 geolocation.
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };

      var config = {
        position: pos
      };

      var marker = new google.maps.Marker({
          position: config.position,
          map: mapa,
          draggable: true
      })
      markers.push(marker);
      mapa.setCenter(pos);

    }, function() {
      handleLocationError(true, infoWindow, mapa.getCenter());
    });
  } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow, mapa.getCenter());
  }
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: El servicio de geolocalizacion no funciono.' :
                        'Error: Tu navegador no posee servicio de geolocalizacion, utiliza Google Chrome en su lugar.');
  infoWindow.open(mapa);
}
