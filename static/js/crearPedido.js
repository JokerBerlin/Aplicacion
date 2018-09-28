$(document).ready(function(){
        $('#id_Total').text("0.00");
        $('#bt_add').click(function(){

            agregar();
            if (document.getElementById("presentacion").length!=0 ) {
              var pre = document.getElementById("presentacion");
              pre.options.length = 0;
              var valorRemove = document.getElementById("valor");
              valorRemove.options.length = 0;
            }
            $('#presentacion').prop('disabled', 'disabled');
            $('#cantidad').prop('disabled', 'disabled');

            $('#inpt-producto').focus();



        });
        $('#bt_add').keypress(function(){
            //agregar();
            $('#inpt-producto').focus();

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
        $("#precioUnitario").change(function(){
                //alert($(this).val());
                //alert("hola");
                //$('#valor2').val($(this).val());
        });

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

    }

    var TotalVenta=0;
    var cont=0;
    var id_fila_selected=[];
    function agregar(){
        cont++;
        Producto = $('#inpt-producto').val();
        codigo = $('#codigo').val();
        precio = $('#precio').val();
        cantidad = $('#cantidad').val();
        error = "";
        if (Producto==''){
            error = 1;
        }

        if (cantidad==''){
            error = 2;
        }
        if (error=="") {
            SubTotal = parseFloat(precio*cantidad).toFixed(2);
            valor = cont - 1;
            var fila='<tr class="selected" id="fila'+valor+'" onclick="seleccionar(this.id);"><td>'+valor+'</td><td><input type="number" name="cantidad'+valor+'" id="cantidad'+valor+'" required="" class="form-control" value="'+cantidad+'"></td><td>'+codigo+'</td><td>'+Producto+'</td><td><input type="number" name="precioUnitario'+valor+'" id="precioUnitario'+valor+'" required="" class="form-control" value="'+precio+'" onchange="CalcularSubTotal('+cont+','+cantidad+')" ></td></td><td><label id="SubTotal'+valor+'" name="SubTotal'+valor+'">'+SubTotal+'</label></td></tr>';
            $('#tabla').append(fila);

            TotalVenta =  parseFloat(Math.round((TotalVenta + (precio*cantidad)) * 100) / 100).toFixed(2);

            //$('#id_Total').text("S/. "+TotalVenta);
            RefrescarTotal();
            reset_values();
            reordenar();

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
        // $('#inpt-producto').focus(function(){
        //   if (document.getElementById("presentacion").length!=0 ) {
        //     var pre = document.getElementById("presentacion");
        //     pre.options.length = 0;
        //     var valorRemove = document.getElementById("valor");
        //     valorRemove.options.length = 0;
        //   }
        //   $('#presentacion').prop('disabled', 'disabled');
        //   $('#cantidad').prop('disabled', 'disabled');
        //
        // });

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
        reordenar();
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
            valor = $(this).find('td').eq(5).children('label').text();
            //console.log(valor);
            Total = Total + parseFloat(valor);
            $('#id_Total').text(Total);
            //alert(Total);
        });
    }

    function eliminarTodasFilas(){
    $('#id_Total').text("0.00");
    $('#tabla tbody tr').each(function(){
            $(this).remove();
        });

    }

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

                    case 1:
                        cantidad = $("#cantidad"+index ).val();
                        break;

                    case 2:
                        codigo = $(this).text();
                        break;
                    case 5:
                        precioVenta = $(this).text();
                        break;
                }

            });
            contador = 1;
            productos.push([cantidad,codigo,precioVenta]);
        });
        console.log(productos);
        var cliente = document.getElementById("inpt-cliente").value;
        if (contador == 1) {
            var datos = {productos: productos,cliente:cliente};
            var sendData = JSON.stringify(datos);
            $.ajax({
                type: "POST",
                dataType: "json",
                url: "/venta/insertar/",
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
