$(document).ready(function(){

  $("#id_nombre").focus();
  var latCliente;
  var longCliente;
  $('#id_nombre').focusout( function(){
      $('#id_cliente').focus();
  });
  $('#id_cliente').focusout( function(){
      $('#bt_add').focus();
  });
  $( "#id_cliente" ).autocomplete({
      source: function (request, response) {
          var datos = {nombreCliente: $("#id_cliente").val()};
          var sendData = JSON.stringify(datos);
          $.ajax({
              type: "POST",
              dataType: "json",
              url: "/cliente/buscar/",
              data: sendData,
              contentType: "application/json; charset=utf-8",
              async: false,
              cache: false,
              CrossDomain: true,

              success: function (result) {
              var ListasClientes = result['clientes'];
              response($.map(ListasClientes, function (item) {

                  return {
                      label: item.nombre,
                      idcliente: item.nombre,
                      direccion: item.direccion,
                      latitud: item.latitud,
                      longitud: item.longitud,
                      Id: item.id
                      };
                  }));
              }
          });
      },

      minLength: 1,

      select: function (event, ui) {
          $.data(document.body, 'idcliente', ui.item.Id);//guardar el id en memoria el $.data guarda en memoria
          // var direccion=  ui.item.direccion;

          var iDPro = ui.item.Id;

          latCliente = ui.item.latitud;
          longCliente = ui.item.longitud;

          $('#latitud').val(latCliente);
          $('#longitud').val(longCliente);
          $('#bt_add').focus();
      }


  });
        $('#id_cliente').focusout( function(){
            $('#bt_add').focus();
        });

        $('#bt_add').click(function(){
            agregar();
            $('#id_cliente').focus();
        });
        $('#bt_add').keypress(function(){
            agregar();
            $('#id_cliente').focus();
        });
        $('#bt_del').click(function(){
            eliminar(id_fila_selected);
        });

        $('#bt_delall').click(function(){
            eliminarTodasFilas();
        });
        $('#bt_GenerarRuta').click(function(){
            agregarRuta();
        });
});


function reset_values(){
    // $('#id_nombre').val('');
    $('#id_cliente').val('');
    $('#latitud').val('');
    $('#longitud').val('');
}

var cont=0;
var id_fila_selected=[];
function agregar(){
    cont++;
    Nombre = $('#id_nombre').val();
    Cliente = $('#id_cliente').val();
    Latitud = $('#latitud').val();
    Longitud = $('#longitud').val();

    error = "";
    if (Cliente==''){
        error = 1;
    }else{
      var nombreClienteAgregar = $('#id_cliente').val();
      $("#tabla tbody tr").each(function (index) {
          $(this).children("td").each(function (index2) {
              producto = [];
              //dato = index;
              console.log(index);
              switch (index2) {
                  case 2:
                      nombreCliente = $(this).text();
                      //alert(tipoPresentacion);
                      //alert(nombreProducto);

                      //
                        if(nombreClienteAgregar === nombreCliente){
                            //if(){
                                alert("Usted ya agrego este cliente");
                                reset_values();
                                error = 3;
                            //}
                        }

                      //}

                      break;
              }

          });
          contador = 1;

          //productos.push([cantidad,codigo,tipoPrecio,presentacion,precioUnitario]);
      });


    }

    if (error=="") {
        // se crea el JSON latLng que contiene las coordenadas de los clientes
        var latLng = [Latitud, Longitud];

        var pos = {lat: parseFloat(Latitud), lng: parseFloat(Longitud)};

        var config = {position: pos};

        addMarker(config);

        var fila =
                '<tr class="selected" id="fila'+cont+'" onclick="seleccionar(this.id);">' +
                '<td>'+cont+'</td>' +
                '<td>'+Nombre+'</td>' +
                '<td>'+Cliente+'</td>' +
                '<td>'+Latitud+'</td>' +
                '<td>'+Longitud+'</td>' +
                '</tr>';
        $('#tabla').append(fila);

        var coordenadas = Array();

        for (let i = 0; i < markers.length; i++) {
            const marker = markers[i];
            const coord = {lat: marker.position.lat(), lng: marker.position.lng()};
            coordenadas.push(coord);
            console.log(coordenadas)
        }

        var waypts = [];
        if (markers.length > 2) {
            for (let index = 1; index < markers.length - 1; index++) {
                waypts.push({
                    location: markers[index].position,
                    stopover: true
                })
            }
        } else {
            waypts = []
        }

        if (waypts.length > 0) {
            ds.route({
                origin: markers[0].position,
                destination: markers[markers.length - 1].position,
                waypoints: waypts,
                optimizeWaypoints: true,
                travelMode: 'DRIVING',
            }, function(response, status) {
                if (status === 'OK') {
                    dr.setDirections(response);
                } else {
                    alert('Error ' + status);
                }
            })
        } else {
            ds.route({
                origin: markers[0].position,
                destination: markers[markers.length - 1].position,
                optimizeWaypoints: true,
                travelMode: 'DRIVING',
            }, function(response, status) {
                if (status === 'OK') {
                    dr.setDirections(response);
                } else {
                    alert('Error ' + status);
                }
            })
        }
        reset_values();
        reordenar();
    } else {
        switch(error) {
        case 1:
            alert("Seleccione un Nombre válido!");
            $( "#id_nombre" ).focus();
            break;

        case 2:
            alert("Seleccione un Cliente válido!");
            $( "#id_cliente" ).focus();
            break;

        }
    }
}

function seleccionar(id_fila){
    if($('#'+id_fila).hasClass('seleccionada')){
        $('#'+id_fila).removeClass('seleccionada');
    }
    else{
        $('#'+id_fila).addClass('seleccionada');
    }
    //2702id_fila_selected=id_fila;
    id_fila_selected.push(id_fila);
}

function eliminar(id_fila){
    /*$('#'+id_fila).remove();
    reordenar();*/
    ValorRestar = 0;
    for(var i=0; i<id_fila.length; i++){
        $('#'+id_fila[i]).children("td").each(function (index2) {
            switch (index2) {
                case 5:
                    ValorRestar = parseFloat($(this).text()).toFixed(2);
                    break;
            }
        });

        $('#'+id_fila[i]).remove();
    }
    reordenar();
}

function reordenar(){
    var num=1;
    $('#tabla tbody tr').each(function(){
        $(this).find('td').eq(0).text(num);
        num++;
    });
}

function eliminarTodasFilas(){

$('#tabla tbody tr').each(function(){
        $(this).remove();
    });

}

function agregarRuta(){
    oRutas = [];
    contador = 0;
    $("#tabla tbody tr").each(function (index) {
        $(this).children("td").each(function (index2) {
            rutas = [];
            switch (index2) {
                case 1:
                    Nombre = $(this).text();
                    break;
                case 2:
                    Cliente = $(this).text();
                    break;

            }
        });
        contador = 1;
        oRutas.push([Nombre,Cliente]);
    });
    console.log(oRutas);
    //var cliente = document.getElementById("id_cliente").value;
    //console.log(cliente)
    if (contador == 1) {
        var datos = {oRutas: oRutas};
        var sendData = JSON.stringify(datos);
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/ruta/insertar/",
            data: sendData,
            contentType: "application/json; charset=utf-8",
            async: false,
            cache: false,
            CrossDomain: true,

            success: function (result) {
                alert('Ruta Registrada');
                document.location.href = '/Ruta/listar/';
                // location.reload(true);
            }
        });
    }else{
        alert("ingrese datos");
        $('#id_cliente').focus();
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
                        'Error: TEl servicio de geolocalizacion no funciono.' :
                        'Error: Tu navegador no posee servicio de geolocalizacion, utiliza Google Chrome en su lugar.');
  infoWindow.open(mapa);
}
