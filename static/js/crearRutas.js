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

var coordenadas = [];

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
        coordenadas.push(latLng);

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

        reset_values();
        reordenar();
    }
    else{
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
/*
function rescatar(){
var valor= document.getElementById("direccion");
    console.log(valor.value);
}


function agregarRuta(){
    var num=1;
    Rutas = [];
    contador = 0;
    $("#tabla tbody tr").each(function (index) {
        $(this).children("td").each(function (index2) {
            rutas = [];
            switch (index2) {
                case 1:
                    nombre = $(this).text();
                    break;
                case 2:
                    cliente = $(this).text();
                    break;
                case 5:
                    direccion = $(this).text();
                    break;
            }
        });
        contador = 1;
        Rutas.push([nombre,cliente,direccion]);
    });
    //console.log(productos);
    if (contador == 1) {
        var datos = {Rutas: Rutass};
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
                var id_ruta = result["id_ruta"];
                alert('Ruta Registrada');
                location.reload(true);
            }
        });
    }else{
        alert("No registró ninguna ruta");
    }
}
**/


function agregarRuta(){
    var num=1;
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
                    document.location.href='/Ruta/listar/';
                // location.reload(true);
            }
        });
    }else{
        alert("ingrese datos");
    }
}


