$(document).ready(function(){
    $('#id_Total').text("0.00");

    $('#inpt-cliente').focusout( function(){
        $('#inpt-producto').focus();
    });
    $('#bt_addVenta').click(function(){
        if(document.getElementById('codigo') === '' || document.getElementById('inpt-producto') === '') {
            reset_values();
            document.getElementById('inpt-producto').focus();
        } else {
            agregar();
        }
        //$('#inpt-producto').focus();
    });

    $('#bt_addVenta').keypress(function(){
        // var nombreProductoAgregar = $('#inpt-producto').val();
        // $("#tabla tbody tr").each(function (index) {
        //     $(this).children("td").each(function (index2) {
        //         producto = [];
        //         //dato = index;
        //         console.log(index);
        //         switch (index2) {
        //             case 4:
        //                 tipoPrecio = $(this).text();
        //                 if(nombreProductoAgregar === tipoPrecio){
        //                     alert("Usted ya agrego este producto");
        //                 }
        //
        //                 break;
        //         }
        //
        //     });
        //     contador = 1;
        //     productos.push([cantidad,codigo,tipoPrecio,presentacion,precioUnitario]);
        // });
        $('#inpt-producto').focus();
    });

    $('#bt_del').click(function(){
        eliminar(id_fila_selected);
        //RefrescarTotal();
    });

    $('#bt_delall').click(function(){
        eliminarTodasFilas();
    });

    $('#bt_GenerarVenta').click(function(){
        // var regexDNI = /^[0-9]{8}$/;
        // var regexRUC = /^[0-9]{11}$/;
        // const clienteDoc = document.getElementById('inpt-cliente').value;
        // const nombreCliente = document.getElementById('nombreCl').value;
        // if (regexDNI.test(clienteDoc)) {
        //     GenerarVenta();
        // } else if (regexRUC.test(clienteDoc)) {
        //     GenerarVenta();
        // } else {
        //     alert('El campo "Cliente" tiene que ser apropiadamente llenado')
        //     x = document.getElementById('inpt-cliente');
        //     x.value = '';
        //     document.getElementById('nombreCl').value = '';
        //     x.focus();
        // }
        GenerarVenta();

    });

    $('#bt_nuevaVenta').click(function() {
        nuevaVenta();
    })

    // VALIDADORES ONKEYPRESS
    x = document.getElementById('inpt-cliente')
    x.addEventListener('keypress', (event) => {
        var valAnterior = x.value;
        console.log(valAnterior)
        const keyName = event.key;
        console.log(keyName);
        if(keyName == 'e') {
            x.value = valAnterior;
        }
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
    $('#inpt-producto').val('');
    $('#codigo').val('');
    $('#precio').val('');
    $('#cantidad').val('');
    $('#valorPrecio').val('');
    $('#inpt-producto').focus();
}

var TotalVenta=0;
var cont=0;
var id_fila_selected=[];
function agregar(){
    cont++;
    Producto = $('#inpt-producto').val();
    console.log(Producto);
    codigo = $('#codigo').val();
    console.log(codigo);
    precio = $('#valorPrecio').val();
    console.log(precio);
    cantidad = $('#cantidad').val();
    console.log(cantidad);
    presentacion = $('#cmbPresentacion').val();
    precioTipo = $('#cmbPrecio').val();
    imagen = $('#urlImagen').val();

    error = "";
    if (Producto==''){
        error = 1;
    }else if(precio=='') {
        error = 2;
    }else if(cantidad==''){
        error = 3;
    }else{
      $("#tabla tbody tr").each(function (index) {
          $(this).children("td").each(function (index2) {
              producto = [];
              console.log(index);
              switch (index2) {
                  case 4:
                      nombreProducto = $(this).text();

                      break;
                  case 6:
                      tipoPresentacion = $(this).text();
                        if((presentacion === tipoPresentacion) && (Producto === nombreProducto) ){
                                  alert("Usted ya agrego este producto");
                                reset_values();
                                error = 4;
                        }
                      break;
              }

          });
          contador = 1;
      });
    }


    if (error=="") {
        SubTotal = parseFloat(precio*cantidad).toFixed(2);
        valor = cont - 1;
        var fila='<tr class="selected" id="fila' + valor + '" onclick="seleccionar(this.id);">' +
                 '<td>' + valor + '</td>' +
                 '<td><img src="'+imagen+'" height="100" width="100" alt="" /></td>'+
                 '<td><input type="number" name="cantidad' + valor + '" id="cantidad' + valor + '" required="" class="form-control" onchange ="eventoCambio('+valor+');" value="' + cantidad + '"></td>' +
                 '<td>' + codigo + '</td>' +
                 '<td>' + Producto + '</td>' +
                 '<td>' + precioTipo+'</td>' +
                 '<td>' + presentacion + '</td>' +
                 '<td id="precioUnitario'+ valor +'">' + precio + '</td>' +
                 '<td><label id="SubTotal' + valor + '" name="SubTotal' + valor + '">' + SubTotal + '</label></td>' +
                 '</tr>';

        $('#tabla').append(fila);

        TotalVenta =  parseFloat(Math.round((TotalVenta + (precio*cantidad)) * 100) / 100).toFixed(2);
        console.log(TotalVenta);

        //$('#id_Total').text("S/. "+TotalVenta);
        RefrescarTotal();
        reset_values();
        //reordenar();
    }else{
        switch(error) {
            case 1:
                alert("Seleccione un producto válido!");
                $( "#inpt-producto" ).focus();
                break;
            case 2:
                alert("No se encuentra la presentación elegida!");
                $( "#cmbPresentacion:first" ).focus();
                break;
            case 3:
                alert("Ingrese una cantidad valida");
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
            switch (index2) {
                case 5:
                    ValorRestar = parseFloat($(this).text()).toFixed(2);
                    break;
            }
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
        valor = $(this).find('td').eq(8)[0].innerText;
        //console.log(valor);
        Total = Total + parseFloat(valor);
        $('#id_Total').text(Total.toFixed(2));
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
    productos = [];
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
                    console.log("esto"+numero);
                case 2:
                    cantidad = $("#cantidad"+numero ).val();
                    break;
                case 3:
                    codigo = $(this).text();
                    break;
                case 5:
                    tipoPrecio = $(this).text();
                    break;
                case 6:
                    presentacion = $(this).text();
                    break;
                case 7:
                    precioUnitario = $(this).text();
                    break;
            }

        });
        contador = 1;
        productos.push([cantidad,codigo,tipoPrecio,presentacion,precioUnitario]);
    });
    console.log(productos);
    var cliente = document.getElementById("inpt-cliente").value;
    if (contador == 1) {
        var datos = {productos: productos,cliente:cliente};
        var sendData = JSON.stringify(datos);
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/Pedido/registrar/",
            data: sendData,
            contentType: "application/json; charset=utf-8",
            async: false,
            cache: false,
            CrossDomain: true,

            success: function (result) {
            //     var id_venta = result["id_venta"];
                 alert('Pedido Registrado');
                 //location.reload(true);
                 document.location.href='/Pedido/listar/';
            }
        });
    }else{
        alert("No registró ningún producto");
    }
}

function imprimir_venta(id_venta){
    window.open('/venta/imprimir/'+id_venta+'/', '_blank');
}


// FUNCION QUE GENERA UNA NUEVA VENTA
function nuevaVenta() {
    var num=1;
    productos = [];
    contador = 0;
    $("#tabla tbody tr").each(function (index) {
        $(this).children("td").each(function (index2) {
            producto = [];
            //dato = index;
            console.log(index);
            switch (index2) {
                case 1:
                    cantidad = $("#cantidad"+index ).val();
                    break;
                case 2:
                    codigo = $(this).text();
                    break;
                case 4:
                    tipoPrecio = $(this).text();
                    break;
                case 5:
                    presentacion = $(this).text();
                    break;
                case 6:
                    precioUnitario = $(this).text();
                    break;
            }

        });
        contador = 1;
        productos.push([cantidad,codigo,tipoPrecio,presentacion,precioUnitario]);
    });
    console.log(productos);
    var cliente = document.getElementById("inpt-cliente").value;
    var tipoRecibo = $('#cmbTipoRecibo').val();
    var nrecibo = $('#nroRecibo').val();
    var cajaId = $('#cmbCaja').val();
    if (contador == 1) {
        var datos = {
            productos: productos,
            cliente: cliente,
            nrecibo: nrecibo,
            tipoRecibo: tipoRecibo,
            cajaId: cajaId
        };

        var sendData = JSON.stringify(datos);
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/Venta/registrar/",
            data: sendData,
            contentType: "application/json; charset=utf-8",
            async: false,
            cache: false,
            CrossDomain: true,

            success: function (result) {
            //     var id_venta = result["id_venta"];
                 alert('Venta Registrada');
                 //location.reload(true);
                 document.location.href='/Venta/listar/';
            }
        });
    }else{
        alert("No registró ningún producto");
    }
}

function eventoCambio(valor){
    var cantidad = $('#cantidad'+valor+'').val();
    console.log(cantidad);
    if (cantidad != ''){
        var precioU = $('#precioUnitario'+valor+'').text();
        console.log(cantidad);
        console.log(precioU);
        var subTot = parseFloat(cantidad) * parseFloat(precioU);
        $('#SubTotal'+valor+'').text(subTot.toFixed(2));
        RefrescarTotal();
    }else{
        alert("Ingrese una cantidad válida");
        $('#cantidad'+valor+'').focus();
    }

}

function agregarProducto(){
  $("#cantidad").keypress(function(e) {
      if(e.which == 13) {
        agregar();
      }
    });
}
