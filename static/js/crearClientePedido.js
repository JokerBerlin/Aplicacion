var marker;
var coords={};

initMap= function() {

  //usamos la API para geolocalización
  navigator.geolocation.getCurrentPosition(
      function (position){

        coords={
          lng: position.coords.longitude,
          lat: position.coords.latitude
        };

        setMapa(coords); //pasamos las coordenadas al método para crear el mapa.

      }, function(error){console.log(error);});
  }

  function setMapa(coords){

  var map=new google.maps.Map(document.getElementById('map'),
  {
    zoom: 13,
    center: new google.maps.LatLng(coords.lat, coords.lng),

  });

  marker = new google.maps.Marker({

    map: map,
    draggable: true,
    animation: google.maps.Animation.DROP,
    position: new google.maps.LatLng(coords.lat, coords.lng),


  });

  marker.addListener('click', toggleBounce);
  marker.addListener('dragend', function(event){
     document.getElementById("id_latitud").value=this.getPosition().lat();
     document.getElementById("id_longitud").value=this.getPosition().lng();
  });

}


function toggleBounce(){

  if(marker.getAnimation() !== null){
    marker.setAnimation(null);
  }else{
    marker.setAnimation(google.maps.Animation.BOUNCE);
  }
}
