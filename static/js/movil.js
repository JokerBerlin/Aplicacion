function convertir(latitude, longitude){
    latitude_sign  = 1;
    longitude_sign = 1;
    if(latitude < 0)
        latitude_sign = -1;
    if(longitude < 0)
        longitude_sign = -1;
    // Validations
    if(latitude > 90 || latitude < -90)
        throw "Latitude.degrees (-90 < d < 90) invalid: " + latitude;
    if(longitude > 180 || longitude < -180)
        throw "Longitude.degrees (-180 < d < 180) invalid: " + longitude;
    // Final calculations
    latitude_deg = Math.floor(Math.abs(latitude));
    latitude_min = Math.floor((Math.abs(latitude) - latitude_deg) * 60);
    latitude_sec = Math.ceil(((Math.abs(latitude) - latitude_deg) * 60 - latitude_min) * 60);
    latitude_dir  = (latitude_sign > 0) ? "N" : "S";
    longitude_deg = Math.floor(Math.abs(longitude));
    longitude_min = Math.floor((Math.abs(longitude) - longitude_deg) * 60);
    longitude_sec = Math.ceil(((Math.abs(longitude) - longitude_deg) * 60 - longitude_min) * 60);
    longitude_dir  = (longitude_sign > 0) ? "E" : "W";
    // Packing the results
    return {
        "latitude": {
            "degrees": Math.abs(latitude_deg),
            "minutes": latitude_min,
            "seconds": Math.round(latitude_sec),
            "dir": latitude_dir
        },
        "longitude": {
            "degrees": Math.abs(longitude_deg),
            "minutes": longitude_min,
            "seconds": Math.round(longitude_sec),
            "dir": longitude_dir
        }
    };
}
    
function ObtenerURL(x, y){
    var coordenadaX= x;
    var coordenadaY= y;
    var URL= "https://www.google.com.pe/maps/place/";
  	var respuesta = convertir(coordenadaX, coordenadaY);
  	var Latitud= respuesta["latitude"]["degrees"]+"\°"+respuesta["latitude"]["minutes"]+"\'"+respuesta["latitude"]["seconds"];
  	var Longitud= respuesta["longitude"]["degrees"]+"\°"+respuesta["longitude"]["minutes"]+"\'"+respuesta["longitude"]["seconds"]+"\""+respuesta["longitude"]["dir"];
  	URL = URL+Latitud+'\"'+respuesta["latitude"]["dir"]+'\+'+Longitud;
  	location.href=URL;
    //alert(URL);
};
/*
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
    });

    function reset_values(){
        $('#id_cliente').val('');
        $('#direccion').val('');
    }

    var cont=0;
    var id_fila_selected=[];
    function agregar(){
        cont++;
        Cliente = $('#id_cliente').val();
        direccion = $('#direccion').val();
        error = "";
        if (Cliente==''){
            error = 1;
        }

        if (error=="") {
            var fila=
            '<tr class="selected" id="fila'+cont+'" onclick="seleccionar(this.id);"><td>'+cont+'</td><td>'+Cliente+'</td><td>'+direccion+'</td></tr>';
            $('#tabla').append(fila);

            reset_values();
            reordenar();
        }
        else{
            switch(error) {
            case 1:
                alert("Seleccione un cliente válido!");
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
        reordenar();
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
*/