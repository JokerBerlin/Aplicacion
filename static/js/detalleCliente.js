var marker;  //variable de marcador

var a= parseFloat('{{oCliente.latitud}}');
var b= parseFloat('{{oCliente.longitud}}');

$( document ).ready(function() {
  console.log( "ready!" );
});

function initMap() {
//const var1= -13.1680054;
//const var2= -74.221639;
    var uluru = {lat: a, lng: b};

    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 10,
      center: uluru
    });
    var marker = new google.maps.Marker({
      position: uluru,
      map: map
    });
}
