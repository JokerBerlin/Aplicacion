$(document).ready(function(){
    $('#bt_add').click(function(){
        agregar();
        $('#inpt-producto').focus();
    });

    $('#bt_add').keypress(function(){
        $('#cmbPresentacion').focus();
    });

    $('#bt_del').click(function(){
        eliminar(id_fila_selected);
    });

    $('#bt_delall').click(function(){
        eliminarTodasFilas();
    });

    $('#bt_GenerarVenta').click(function(){
        GenerarVenta();
    });

    $('#bt_nuevaVenta').click(function() {
        nuevaVenta();
    })

});

function CalcularSubTotal(id,cantidad){
    SubTotal = $('#precioUnitario'+id).val()*cantidad;
    SubTotal = parseFloat(SubTotal).toFixed(2);
    $('#SubTotal'+id).text(SubTotal);
    RefrescarTotal();
    //console.log($(this));
}
function reset_values(){
    $('#cantPresentacion').val('');
    $('#1Precio').val('');
    $('#2Precio').val('');
    $('#3Precio').val('');
}


var cont=0;
var id_fila_selected=[];
function agregar(){
    cont++;
    var combo = document.getElementById("cmbPresentacion");
    presentacion = combo.options[combo.selectedIndex].text;
    cantidadPrincipal = $('#cantPresentacion').val();
    precio1 = $('#1Precio').val();
    precio2 = $('#2Precio').val();
    precio3 = $('#3Precio').val();

    error = "";
    if (presentacion==''){
        error = 1;
    }

    if (cantidadPrincipal==''){
        error = 2;
    }
    if (precio1==''){
        error = 3;
    }
    if (precio2==''){
        error = 4;
    }
    if (precio3==''){
        error = 5;
    }
    if (error=="") {
        //SubTotal = parseFloat(precio*cantidad).toFixed(2);
        valor = cont - 1;
        var fila='<tr class="selected" id="fila' + valor + '" onclick="seleccionar(this.id);">' +
                 '<td>' + valor + '</td>' +
                 '<td>' + presentacion + '</td>' +
                 '<td><input type="number" name="cantidadPrincipal' + valor + '" id="cantidadPrincipal' + valor + '" required="" class="form-control" value="' + cantidadPrincipal + '"></td>' +
                 '<td><input type="number" name="precio1' + valor + '" id="precio1' + valor + '" required="" class="form-control" value="' + precio1 + '"></td>' +
                 '<td><input type="number" name="precio2' + valor + '" id="precio2' + valor + '" required="" class="form-control" value="' + precio2 + '"></td>' +
                 '<td><input type="number" name="precio2' + valor + '" id="precio3' + valor + '" required="" class="form-control" value="' + precio3 + '"></td>' +
                 '</tr>';

        $('#tabla').append(fila);


        //$('#id_Total').text("S/. "+TotalVenta);
        RefrescarTotal();
        reset_values();
        //reordenar();
    }
    else{
        switch(error) {
        case 1:
            alert("Seleccione un producto válido!");
            $( "#inpt-producto" ).focus();
            break;
        case 2:
            alert("Ingrese una cantidad");
            $( "#cantidad" ).focus();
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
            //switch (index2) {
              //  case 5:
              //      ValorRestar = parseFloat($(this).text()).toFixed(2);
              //      break;
            //}
        });
        //TotalVenta = TotalVenta - ValorRestar
        //$('#id_Total').text("S/. "+TotalVenta);
        RefrescarTotal();
        $('#'+id_fila[i]).remove();
    }
    //reordenar();
}

function reordenar(){
    var num=1;
    $('#tabla tbody tr').each(function(){
        $(this).find('td').eq(0).text(num);
        num++;
    });

}

function RefrescarTotal(){
    Total=0;
    $('#tabla tbody tr').each(function(){
        //valor = $(this).find('td').eq(5).children('label').text();
        //console.log(valor);
        //Total = Total + parseFloat(valor);
        //$('#id_Total').text(Total);
        //alert(Total);
    });
}

function eliminarTodasFilas(){
$('#id_Total').text("0.00");
$('#tabla tbody tr').each(function(){
        $(this).remove();
    });
}

// GENERA UN NUEVO PEDIDO
function GenerarVenta(){
    var num=1;
    presentaciones = [];
    contador = 0;
    $("#tabla tbody tr").each(function (index) {
        $(this).children("td").each(function (index2) {
            producto = [];
            //dato = index;
            console.log(index);
            switch (index2) {
                case 0:
                    numero = $(this).text();
                    numero = parseInt(numero);
                case 1:
                    presentacion = $(this).text();
                    break;
                case 2:
                    cantidadPrincipal = $("#cantidadPrincipal"+numero ).val();
                    break;
                case 3:
                    precio1 = $("#precio1"+numero ).val();
                    break;
                case 4:
                    precio2 = $("#precio2"+numero ).val();
                    break;
                case 5:
                    precio3 = $("#precio3"+numero ).val();
                    break;
            }

        });
        contador = 1;
        presentaciones.push([presentacion,cantidadPrincipal,precio1,precio2,precio3]);
    });
    console.log(presentaciones);
    var producto = document.getElementById("productoId").value;
    if (contador == 1) {
        var datos = {presentaciones: presentaciones,producto:producto};
        var sendData = JSON.stringify(datos);
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/Presentacion/nuevo/",
            data: sendData,
            contentType: "application/json; charset=utf-8",
            async: false,
            cache: false,
            CrossDomain: true,

            success: function (result) {
            //     var id_venta = result["id_venta"];
                 alert('Presentaciones Registradas');
                 //location.reload(true);
                 document.location.href='/Producto/listar/';
            }
        });
    }else{
        alert("No registró ninguna presentación");
    }
}

function imprimir_venta(id_venta){
    window.open('/venta/imprimir/'+id_venta+'/', '_blank');
}
