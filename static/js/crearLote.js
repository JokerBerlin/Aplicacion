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

        $('#bt_GenerarVenta').click(function(){
            GenerarLote();
        });

    });

    function reset_values(){
        //$('#inpt-proveedor').val('');
       // $('#inpt-recibo').val('');
        $('#inpt-almacen').val('');
        $('#inpt-producto').val('');
        $('#cantidad').val('');

    }
    var cont=0;
    var id_fila_selected=[];
    function agregar(){
        cont++;
        Proveedor = $('#inpt-proveedor').val();
        Recibo = $('#inpt-recibo').val();
        Almacen = $('#inpt-almacen').val();
        Producto = $('#inpt-producto').val();
        cantidad = $('#cantidad').val();

        error = "";
        if (cantidad==''){
            error = 1;
        }

        if (Proveedor==''){
            error = 2;
        }

        if (Recibo==''){
            error = 3;
        }
        if (Almacen==''){
            error = 4;
        }
        if (Producto==''){
            error = 5;
        }
    
        if (error=="") {
            var fila=
            '<tr class="selected" id="fila'+cont+'" onclick="seleccionar(this.id);"><td>'+cont+'</td><td>'+cantidad+'</td><td>'+Proveedor+'</td><td>'+Recibo+'</td><td>'+Almacen+'</td><td>'+Producto+'</td></tr>';
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
                switch (index2) {
                    case 1:
                        cantidad = $(this).text();
                        break;
                    case 4:
                        Almacen = $(this).text();
                        break;
                    case 5:
                        Producto = $(this).text();
                        break;

                }
            });
            contador = 1;
            oProductoAlmacen.push([cantidad,Almacen, Producto]);
        });
        var oProveedor = document.getElementById("inpt-proveedor").value;
        var oRecibo = document.getElementById("inpt-recibo").value;
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
                     //location.reload(true);
                     //document.location.href='/Pedido/listar/';
                }
            });
        }else{
            alert("No registró ningún lote");
        }
    }
