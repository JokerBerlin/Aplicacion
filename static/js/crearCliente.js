$(document).ready(function(){
		$('#id_nombre').focus();
});

var marker, infoWindow;
var mapa;

var	initMap = function() {
	mapa = new google.maps.Map(document.getElementById('map'), {
		center: {lat: -13.1587800, lng: -74.2232100},
		zoom: 17
	});

	infoWindow = new google.maps.InfoWindow;

	if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };

      var config = {
        position: pos
      };

      marker = new google.maps.Marker({
          position: config.position,
		  map: mapa,
		  animation: google.maps.Animation.DROP,
          draggable: true
      })
	  mapa.setCenter(pos);

	document.getElementById('id_latitud').value = marker.getPosition().lat();
	document.getElementById('id_longitud').value = marker.getPosition().lng();
	marker.addListener('click', toggleBounce);
	marker.addListener('dragend', function(event){
		document.getElementById("id_latitud").value=this.getPosition().lat();
		document.getElementById("id_longitud").value=this.getPosition().lng();
	});


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
                        'Error: TEl servicio de geolocalizacion no funciono.' :
                        'Error: Tu navegador no posee servicio de geolocalizacion, utiliza Google Chrome en su lugar.');
  infoWindow.open(mapa);
}

function toggleBounce(){

	if(marker.getAnimation() !== null){
		marker.setAnimation(null);
	}else{
		marker.setAnimation(google.maps.Animation.BOUNCE);
	}
}
