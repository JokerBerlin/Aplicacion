$(document).ready(function(){
	var nuevo = $('#id_nombre').val();
	$('#id_nombre').val('');
	$('#id_nombre').val(nuevo);
	$('#id_nombre').focus();

  console.log(a);


});

function initMap() {
	var uluru = {lat: a, lng: b};

	var map = new google.maps.Map(document.getElementById('map'), {
		zoom: 15,
		center: uluru
	});
	var marker = new google.maps.Marker({
		position: uluru,
		map: map,
		draggable: true,
	});

	marker.addListener('dragend', function() {
		var lat = this.getPosition().lat();
		var lng = this.getPosition().lng();

		var latitud = document.getElementById('id_latitud').value = lat;
		var longitud = document.getElementById('id_longitud').value = lng;
	})
}
