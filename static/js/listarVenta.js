//datepicker
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

  $( function() {
    $.datepicker.setDefaults($.datepicker.regional['es']);
    $( "#desde" ).datepicker({onSelect: function() {
      var nue = document.getElementById("desde").value;
      console.log(nue);
      var datos = {fechaInicio: nue};
      var sendData = JSON.stringify(datos);
      $.ajax({
          type: "POST",
          dataType: "json",
          url: "/venta/filtrase/",
          data: sendData,
          contentType: "application/json; charset=utf-8",
          async: false,
          cache: false,
          CrossDomain: true,
          success: function (result) {

          }
    });
    $("#btn_bsc").click();
  }
});
    $( "#hasta" ).datepicker({onSelect: function() {
      var nue = document.getElementById("hasta").value;
      console.log(nue);
      var datos = {fechaFin: nue};
      var sendData = JSON.stringify(datos);
      $.ajax({
          type: "POST",
          dataType: "json",
          url: "/venta/filtrase/",
          data: sendData,
          contentType: "application/json; charset=utf-8",
          async: false,
          cache: false,
          CrossDomain: true,
          success: function (result) {

          }
    });
    $("#btn_bsc").click();
  }
});

  } );
});




//filtrar producto por nombre
$(document).ready(function(){
  $( "#inpt-producto" ).focus();
  $( "#inpt-producto" ).autocomplete({
      source: function (request, response) {

          var datos = {nombreProducto: $("#inpt-producto").val()};
          var sendData = JSON.stringify(datos);
          $.ajax({
              type: "POST",
              dataType: "json",
              url: "/producto/buscar/",
              data: sendData,
              contentType: "application/json; charset=utf-8",
              async: false,
              cache: false,
              CrossDomain: true,
              success: function (result) {
              var ListasProductos = result['productos'];
              response($.map(ListasProductos, function (item) {
                  return {label: item.nombre};
                  }));
              }
          });
      },
      minLength: 1,
      select: function (event, ui) {
          //$('#inpt-producto').focus();
          // de tu elemento
          //var nue = document.getElementById("inpt-producto").value;
          //console.log(nue);
          var nue = document.getElementById("inpt-producto").value;
          console.log(nue);
          var datos = {nombreProductos: nue};
          var sendData = JSON.stringify(datos);
          $.ajax({
              type: "POST",
              dataType: "json",
              url: "/venta/filtrase/",
              data: sendData,
              contentType: "application/json; charset=utf-8",
              async: false,
              cache: false,
              CrossDomain: true,
              success: function (result) {

              }
        });
        $("#btn_bsc").click();
      }
});
});


//filtro de clientes por dni o numero documento ajax

$(document).ready(function(){
  $( "#inpt-cliente" ).autocomplete({
      source: function (request, response) {

          var datos = {nombreCliente: $("#inpt-cliente").val()};
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
                var valorCliente = document.getElementById('inpt-cliente').value;
                if( isNaN(valorCliente) ){
                    return {label: item.nombre};
                }else{
                    return {label: item.numerodocumento};
                }
                }));

              }
          });
      },
      minLength: 1,
      select: function (event, ui) {
          //$('#inpt-producto').focus();
          // de tu elemento
          //var nue = document.getElementById("inpt-producto").value;
          //console.log(nue);
          var nue = document.getElementById("inpt-cliente").value;
          console.log(nue);
          var datos = {nombreClientes: nue};
          var sendData = JSON.stringify(datos);
          $.ajax({
              type: "POST",
              dataType: "json",
              url: "/venta/filtrase/",
              data: sendData,
              contentType: "application/json; charset=utf-8",
              async: false,
              cache: false,
              CrossDomain: true,
              success: function (result) {

              }
        });
        $("#btn_bsc").click();
      }
  });
});

$('#btn_buscar').keypress(function(e) {
    var keycode = (e.keyCode ? e.keyCode : e.which);
    if (keycode == '13') {
        e.preventDefault();

    }
});

  $(document).ready(function(){
    $('#btn_buscar').click(function(){
        BuscarProductos();
    });
    $("#close").click(function(){
        $("#producto").hide();
        var datos = {"csrfmiddlewaretoken": "{{ csrf_token }}",nombreProductos: 'eliminar'};
        var sendData = JSON.stringify(datos);
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/venta/filtrar/eliminar/",
            data: sendData,
            contentType: "application/json; charset=utf-8",
            async: false,
            cache: false,
            CrossDomain: true,
            success: function (result) {

            }
      });
      //location.reload(true);
    });
    $("#close2").click(function(){
        $("#cliente").hide();
        var datos = {nombreClientes: 'eliminar'};
        var sendData = JSON.stringify(datos);
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/venta/filtrar/eliminar/",
            data: sendData,
            contentType: "application/json; charset=utf-8",
            async: false,
            cache: false,
            CrossDomain: true,
            success: function (result) {

            }
      });
      location.reload(true);
    });
    $("#close3").click(function(){
        $("#inicio").hide();
        var datos = {fechaInicio: 'eliminar'};
        var sendData = JSON.stringify(datos);
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/venta/filtrar/eliminar/",
            data: sendData,
            contentType: "application/json; charset=utf-8",
            async: false,
            cache: false,
            CrossDomain: true,
            success: function (result) {

            }
      });
      location.reload(true);
    });
    $("#close4").click(function(){
        $("#fin").hide();
        var datos = {fechaFin: 'eliminar'};
        var sendData = JSON.stringify(datos);
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/venta/filtrar/eliminar/",
            data: sendData,
            contentType: "application/json; charset=utf-8",
            async: false,
            cache: false,
            CrossDomain: true,
            success: function (result) {

            }
      });
      location.reload(true);
    });
  });

  function BuscarProductos(){
      var producto = document.getElementById("inpt-producto").value;
      var cliente = document.getElementById("inpt-cliente").value;
      var desde = document.getElementById("desde").value;
      var hasta = document.getElementById("hasta").value;
      var datos = {producto: producto,cliente:cliente,desde:desde,hasta:hasta};
      var sendData = JSON.stringify(datos);
      $.ajax({
          type: "POST",
          dataType: "json",
          url: "/venta/filtrar/",
          data: sendData,
          contentType: "application/json; charset=utf-8",
          async: false,
          cache: false,
          CrossDomain: true,

          success: function (result) {
          //     var id_venta = result["id_venta"];
              var listarV = result["oProductos"];
              var listarV2 = result["oVenta"];
              console.log(listarV);
              console.log(listarV2);
              console.log("hola mundo");
              var ls = Array.from(listarV2);
              console.log(ls);

              for (var i in listarV) {
                  var fila = '<tr>'+
                    '<td>'+listarV[i].id+'</td>'+
                    '<td>'+listarV[i].producto+'</td>'+
                    '</tr>';
                  console.log(listarV[i].producto);
                  $("#tVentas").append(fila);
              }


              for (var i = 0; i < listarV2.length; i++) {

                  console.log(listarV2[i].fecha);


              }



          }
      });

  }
