$(document).ready(function(){
        $( "#cmbAlmacen" ).blur(function() {
          $('#inpt-producto').focus();
        });
        $('#bt_add').click(function(){
            agregar();
            $('#inpt-producto').focus();
        });
        $('#bt_add').keypress(function(e){
            if(e.which == 13) {
                $('#inpt-producto').focus();
            }
        });
        $('#bt_del').click(function(){
            eliminar(id_fila_selected);
        });
        $('#bt_delall').click(function(){
            eliminarTodasFilas();
        });

        $('#bt_GenerarVenta').click(function(){
            GenerarLote();
        });
        $('#inpt-producto').keypress(function(e){
            if(e.keyCode == 13){
               $('#cantidad').focus();
            }

        });

    });

    function reset_values(){
        //$('#inpt-proveedor').val('');
       // $('#inpt-recibo').val('');
       // $('#inpt-almacen').val('');
        $('#inpt-producto').val('');
        $('#cantidad').val('');

    }
    var cont=0;
    var id_fila_selected=[];
    function agregar(){
        cont++;
        var combo = document.getElementById("cmbAlmacen");
        Almacen = combo.options[combo.selectedIndex].text;
        //Almacen = document.getElementById("cmbAlmacen").value;
        Producto = $('#inpt-producto').val();
        cantidad = $('#cantidad').val();
        imagen = $('#urlImagen').val();
        error = "";
        if (cantidad==''){
            error = 1;
        }

        if (Almacen==''){
            error = 2;
        }
        if (Producto==''){
            error = 3;
        }

        if (error=="") {
            valor = cont - 1;
            var fila=
            '<tr class="selected" id="fila'+cont+'" onclick="seleccionar(this.id);"><td>'+cont+'</td>'+
            '<td><img src="'+imagen+'" height="100" width="100" alt="" /></td>'+
            '<td>'+Producto+'</td>'+
            '<td><input type="number" name="cantidad' + valor + '" id="cantidad' + valor + '" required="" class="form-control" value="' + cantidad + '"></td><td>'+Almacen+'</td>'+'</tr>';
            $('#tabla').append(fila);

            reset_values();
            reordenar();
        }
        else{
            switch(error) {
            case 1:
                alert("Ingrese una cantidad");
                $( "#cantidad" ).focus();
                break;

            case 2:
                alert("Seleccione un Proveedor válido!");
                $( "#inpt-proveedor" ).focus();
                break;
            case 3:
                alert("Ingrese un recibo válido");
                $( "#inpt-recibo" ).focus();
                break;

            case 4:
                alert("Ingrese un almacen válido");
                $( "#inpt-almacen" ).focus();
                break;

            case 5:
                alert("Ingrese un producto válido");
                $( "#inpt-producto" ).focus();
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

        for(var i=0; i<id_fila.length; i++){
            //TotalVenta = TotalVenta - ValorRestar
            //$('#id_Total').text("S/. "+TotalVenta);
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

    function GenerarLote(){
        var num=1;
        oProductoAlmacen = [];
        contador = 0;
        $("#tabla tbody tr").each(function (index) {
            $(this).children("td").each(function (index2) {
                lotes = [];
                cont= index -1;
                console.log(index);
                switch (index2) {
                    case 2:
                        Producto = $(this).text();
                        break;
                    case 3:
                        cantidad = $("#cantidad"+index ).val();
                        break;
                    case 4:
                        Almacen = $(this).text();
                        break;
                }
            });
            contador = 1;
            oProductoAlmacen.push([cantidad,Almacen, Producto]);
        });
        console.log(oProductoAlmacen);
        var oProveedor = document.getElementById("inpt-proveedor").value;
        console.log(oProveedor);
        var comboRecibo = document.getElementById("cmbRecibo");
        var oRecibo = comboRecibo.options[comboRecibo.selectedIndex].text;
        console.log(oRecibo);
        //var oPresentacion = document.getElementById("presentacion").value;
        if (contador == 1) {
            var datos = {oProductoAlmacen: oProductoAlmacen, oProveedor: oProveedor, oRecibo: oRecibo};
            var sendData = JSON.stringify(datos);
            $.ajax({
                type: "POST",
                dataType: "json",
                url: "/lote/insertar/",
                data: sendData,
                contentType: "application/json; charset=utf-8",
                async: false,
                cache: false,
                CrossDomain: true,

                success: function (result) {
                //     var id_venta = result["id_venta"];
                     alert('Lote Registrado');
                     document.location.href='/Lote/listar/';

                     //location.reload(true);
                     //document.location.href='/Pedido/listar/';
                }
            });
        }else{
            alert("No registró ningún lote");
        }
    }

function seleccionarProducto(idProducto){
    //alert($('#dynamic'+idProducto+'').attr('src'));
    $('#urlImagen').val($('#dynamic'+idProducto+'').attr('src'));
    $('#producto'+idProducto+'').text();
    //alert($('#producto'+idProducto+'').text());
    $('#inpt-producto').val($('#producto'+idProducto+'').text());
    //$('#codigo').val($('#codigo'+idProducto+'').text());
    $("#imagenesProd").empty();
    $("#cantidad").focus();
}
