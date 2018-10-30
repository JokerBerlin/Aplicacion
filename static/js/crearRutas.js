$(document).ready(function(){

        $('#bt_add').click(function(){
            agregar();
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
        if (markers.length > 2){
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
                optimizeWaypoints: false,
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
                optimizeWaypoints: false,
                travelMode: 'DRIVING',
            }, function(response, status){
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
    }
}


