$(document).ready(function(){
  $.datepicker.regional['es'] = {
    closeText: 'Cerrar',
    prevText: '< Ant',
    nextText: 'Sig >',
    currentText: 'Hoy',
    monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
    monthNamesShort: ['Ene','Feb','Mar','Abr', 'May','Jun','Jul','Ago','Sep', 'Oct','Nov','Dic'],
    dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
    dayNamesShort: ['Dom','Lun','Mar','Mié','Juv','Vie','Sáb'],
    dayNamesMin: ['Do','Lu','Ma','Mi','Ju','Vi','Sá'],
    weekHeader: 'Sm',
    dateFormat: 'dd-mm-yy',
    firstDay: 1,
    isRTL: false,
    showMonthAfterYear: false,
    yearSuffix: ''
  };


  $.datepicker.setDefaults($.datepicker.regional['es']);
  $( "#fechaVencimiento" ).datepicker();

  $( "#inpt-proveedor" ).focus();
  $('#myModal').on('shown.bs.modal', function () {
      $('#id_nombre').trigger('focus');
  });
  $('#myModalProducto').on('shown.bs.modal', function () {

      window.frames['upload'].document.getElementById('id_nombre').focus();
      window.frames['upload'].document.getElementById('itemsProducto').className = "collapse";

  });

  $('#myModalProducto').on('hidden.bs.modal', function () {
      $('#inpt-producto').focus();
  });

  $( "#inpt-producto" ).autocomplete({
      source: function (request, response) {

          var datos = {nombreProducto: $("#inpt-producto").val()};
          var sendData = JSON.stringify(datos);
          $.ajax({
              type: "POST",
              dataType: "json",
              url: "/productopre/buscar/",
              data: sendData,
              contentType: "application/json; charset=utf-8",
              async: false,
              cache: false,
              CrossDomain: true,

              success: function (result) {

                var ListasProductos = result['productos'];
                var ListarPresentaciones = result['presentacion'];

                $("#imagenesProd").empty();
                console.log(ListasProductos);
                a = 1;
                for (var i = 0; i < ListasProductos.length; i+=1) {
                    var img = $('<img id="dynamic'+ListasProductos[i].id+'">'); //Equivalent: $(document.createElement('img'))
                    var br = $('<br/>');
                    a = a + 1;
                    var panelBody = $(' <div tabindex="'+a+'" onkeypress="seleccionarProducto('+ListasProductos[i].id+');" id="dynamicPanelPrincipal'+ListasProductos[i].id+'" class="panel-default col-xs-12 col-sm-12 col-md-12" style="border: 0.05px solid #ECECEC;">');
                    var cierreBody = $('</div>');
                    var panelBody2 = $('<div id="dynamicPanel'+ListasProductos[i].id+'" onclick="seleccionarProducto('+ListasProductos[i].id+');" class="panel-body">');
                    panelBody.appendTo('#imagenesProd');
                    var labelP = $('<label id="producto'+ListasProductos[i].id+'" for="male">'+ListasProductos[i].nombre+'</label>');
                    var labelP2 = $('<label id="codigo'+ListasProductos[i].id+'" for="male1" style="visibility:hidden;">'+ListasProductos[i].codigo+'</label>');
                    var pre = $('<pre>'+ListasProductos[i].codigo+'</pre>');
                    panelBody2.appendTo("#dynamicPanelPrincipal"+ListasProductos[i].id+"");

                    img.attr('src', ListasProductos[i].imagen);
                    img.attr('onclick', 'seleccionarProducto('+ListasProductos[i].id+')');
                    img.attr('height', "50");
                    img.attr('width', "50");
                    img.appendTo("#dynamicPanel"+ListasProductos[i].id+"");
                    labelP.appendTo("#dynamicPanel"+ListasProductos[i].id+"");
                    labelP2.appendTo("#dynamicPanel"+ListasProductos[i].id+"");
                }

                response($.map(ListasProductos, function (item) {
                    return {
                        idproducto: item.nombre,
                        Id: item.id,
                        imagen: item.imagen,
                        };
                    })
                  );

                }
            });
      },
      minLength: 2,
      select: function (event, ui) {
          $.data(document.body, 'idproducto', ui.item.Id);//guardar el id en memoria el $.data guarda en memoria
          $('#cantidad').focus();
      }


  });
  $( "#inpt-proveedor" ).autocomplete({
    source: function (request, response) {

    var datos = {nombreProveedor: $("#inpt-proveedor").val()};
    var sendData = JSON.stringify(datos);
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/proveedor/buscar/",
        data: sendData,
        contentType: "application/json; charset=utf-8",
        async: false,
        cache: false,
        CrossDomain: true,

        success: function (result) {
        var ListasProveedores = result['proveedores'];
        if( Object.keys(ListasProveedores).length === 0 ){
            var numeroNuevo = $('#inpt-proveedor').val();
            var proveedor = new Object();
            proveedor.documento = "nuevo";
            proveedor.nombre = "nuevo";
            proveedor.direccion = numeroNuevo;
            ListasProveedores.push(proveedor);
        }
        response($.map(ListasProveedores, function (item) {
           var valorProveedor = document.getElementById('inpt-proveedor').value;
           return {label: item.documento,
                 nombreP: item.nombre,
               dniP: item.direccion,};
              }));
          }
      });
  },
  minLength: 2,
  select: function (event, ui) {
    if(ui.item.nombreP === "nuevo"){
        if(isNaN(ui.item.dniP)){
          $('#id_nombre').val(ui.item.dniP);
          $('#nuevoProveedor').click();
        }else{
          $('#id_numerodocumento').val(ui.item.dniP);
          $('#nuevoProveedor').click();
        }

    } else{
        $("#inpt-nombreProveedor").val(ui.item.nombreP);
        $('#cmbRecibo').focus();
    }
}

});
        $( "#cmbAlmacen" ).blur(function() {
          $('#fechaVencimiento').focus();
        });
        $( "#fechaVencimiento" ).blur(function() {
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
        $('#precioCompra').val('');

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
        numerRecibo = $('#numeroRecibo').val();
        precioCompra = $('#precioCompra').val();
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
        if (numeroRecibo==''){
            error = 6;
        }
        if (precioCompra==''){
            error = 7;
        }


        if (error=="") {
            valor = cont - 1;
            var fila=
            '<tr class="selected" id="fila'+cont+'" onclick="seleccionar(this.id);"><td>'+cont+'</td>'+
            '<td><img src="'+imagen+'" height="100" width="100" alt="" /></td>'+
            '<td>'+Producto+'</td>'+
            '<td><input type="number" name="cantidad' + valor + '" id="cantidad' + valor + '" required="" class="form-control" value="' + cantidad + '"></td>'+
            '<td><input type="number" name="precioCompra' + valor + '" id="precioCompra' + valor + '" required="" class="form-control" value="' + precioCompra + '"></td>'+
            '<td>'+Almacen+'</td>'+'</tr>';
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
            case 6:
                alert("Ingrese un número de recibo válido");
                $( "#numerRecibo" ).focus();
                break;
            case 7:
                alert("Ingrese un precio de compra válido");
                $( "#precioCompra" ).focus();
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
                        precioCompra = $("#precioCompra"+index ).val();
                        break;
                    case 5:
                        Almacen = $(this).text();
                        break;
                }
            });
            contador = 1;
            oProductoAlmacen.push([cantidad,Almacen, Producto, precioCompra]);
        });
        console.log(oProductoAlmacen);
        var oProveedor = document.getElementById("inpt-proveedor").value;
        console.log(oProveedor);
        var comboRecibo = document.getElementById("cmbRecibo");
        var oRecibo = comboRecibo.options[comboRecibo.selectedIndex].text;
        var oNumeroRecibo = document.getElementById("numeroRecibo").value;
        var oFechaVen = document.getElementById("fechaVencimiento").value;

        if (contador == 1) {
            var datos = {oProductoAlmacen: oProductoAlmacen, oProveedor: oProveedor, oRecibo: oRecibo, oNumeroRecibo: oNumeroRecibo, oFechaVen: oFechaVen,};
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

function RegistrarProveedor(){
  var nombre = document.getElementById("id_nombre").value;
  var direccion = document.getElementById("id_direccion").value;
  var documento = document.getElementById("id_numerodocumento").value;
  console.log(documento);
  var datos = {nombre: nombre,direccion:direccion,documento:documento};
  var sendData = JSON.stringify(datos);
  $.ajax({
      type: "POST",
      dataType: "json",
      url: "/Proveedor/Registrar/",
      data: sendData,
      contentType: "application/json; charset=utf-8",
      async: false,
      cache: false,
      CrossDomain: true,

      success: function (result) {
      //     var id_venta = result["id_venta"];
           alert('El proveedor se registro con exito');
           var numDocumento = $("#id_numerodocumento").val();
           $('#inpt-proveedor').val(numDocumento);
          var nombrePro = $("#id_nombre").val();
           $('#inpt-nombreProveedor').val(nombrePro.toLowerCase());


           $('#myModal').modal('toggle');
           $('#id_nombre').val('');
           $('#id_direccion').val('');
           $('#id_numerodocumento').val('');
           //location.reload(true);
           $('#cmbRecibo').focus();
      }
  });
}
