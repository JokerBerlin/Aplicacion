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
      }
  });
});

$('#btn_buscar').keypress(function(e) {
    var keycode = (e.keyCode ? e.keyCode : e.which);
    if (keycode == '13') {
        e.preventDefault();

    }
});

//Url de busqueda
  // function modificar_url(){
  //     var productoText= document.getElementById("inpt-producto").value;
  //     var clienteText = document.getElementById("inpt-cliente").value;
  //     var desdeText = document.getElementById("desde").value;
  //     var hastaText = document.getElementById("hasta").value;
  //     if(productoText!=''&&clienteText!=''&&desdeText!=''&&hastaText!=''){
  //       document.forms.buscar_filtro.action =  "/venta/filtrar/producto/"+productoText+"/cliente/"+clienteText+"/desde/"+desdeText+"/hasta/"+hastaText+"/" ;
  //     } else if(productoText!=''&&clienteText!=''&&desdeText!=''&&hastaText==''){
  //       document.forms.buscar_filtro.action =  "/venta/filtrar/producto/"+productoText+"/cliente/"+clienteText+"/desde/"+desdeText+"/" ;
  //     } else if(productoText!=''&&clienteText!=''&&desdeText==''&&hastaText!=''){
  //       document.forms.buscar_filtro.action =  "/venta/filtrar/producto/"+productoText+"/cliente/"+clienteText+"/hasta/"+hastaText+"/" ;
  //     } else if(productoText!=''&&clienteText==''&&desdeText!=''&&hastaText!=''){
  //       document.forms.buscar_filtro.action =  "/venta/filtrar/producto/"+productoText+"/desde/"+desdeText+"/hasta/"+hastaText+"/" ;
  //     } else if(productoText!=''&&clienteText==''&&desdeText!=''&&hastaText==''){
  //       document.forms.buscar_filtro.action =  "/venta/filtrar/producto/"+productoText+"/desde/"+desdeText+"/" ;
  //     } else if(productoText!=''&&clienteText==''&&desdeText==''&&hastaText!=''){
  //       document.forms.buscar_filtro.action =  "/venta/filtrar/producto/"+productoText+"/hasta/"+hastaText+"/" ;
  //     } else if(productoText==''&&clienteText!=''&&desdeText!=''&&hastaText!=''){
  //       document.forms.buscar_filtro.action =  "/venta/filtrar/cliente/"+clienteText+"/desde/"+desdeText+"/hasta/"+hastaText+"/" ;
  //     } else if(productoText==''&&clienteText!=''&&desdeText!=''&&hastaText==''){
  //       document.forms.buscar_filtro.action =  "/venta/filtrar/cliente/"+clienteText+"/desde/"+desdeText+"/" ;
  //     } else if(productoText==''&&clienteText!=''&&desdeText==''&&hastaText!=''){
  //       document.forms.buscar_filtro.action =  "/venta/filtrar/cliente/"+clienteText+"/hasta/"+hastaText+"/" ;
  //     } else if(productoText!=''&&clienteText!=''&&desdeText==''&&hastaText==''){
  //       document.forms.buscar_filtro.action =  "/venta/filtrar/producto/"+productoText+"/cliente/"+clienteText+"/" ;
  //     } else if(productoText==''&&clienteText==''&&desdeText!=''&&hastaText!=''){
  //       document.forms.buscar_filtro.action =  "/venta/filtrar/desde/"+desdeText+"/hasta/"+hastaText+"/" ;
  //     } else if(productoText!=''&&clienteText==''&&desdeText==''&&hastaText==''){
  //       document.forms.buscar_filtro.action =  "/venta/filtrar/producto/"+productoText+"/" ;
  //     }  else if(productoText==''&&clienteText!=''&&desdeText==''&&hastaText==''){
  //       document.forms.buscar_filtro.action =  "/venta/filtrar/cliente/"+clienteText+"/" ;
  //     }  else if(productoText==''&&clienteText==''&&desdeText!=''&&hastaText==''){
  //       document.forms.buscar_filtro.action =  "/venta/filtrar/desde/"+desdeText+"/" ;
  //     }  else if(productoText==''&&clienteText==''&&desdeText==''&&hastaText!=''){
  //       document.forms.buscar_filtro.action =  "/venta/filtrar/hasta/"+hastaText+"/" ;
  //     }
  //   }

  $(document).ready(function(){
    $('#btn_buscar').click(function(){
        BuscarProductos();
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


              // for (var j in listarV2) {
              //
              //     console.log(listarV2[j][0][0]);
              // }


              // for (x=0;x<listarV.length;x++){
              //     document.write(listarV[x] + " ");
              // }
              // for (var variable in listarV) {
              //   var a = variable.id;
              //   Console.log(variable);
              //
              // }
               //alert(a);
               //location.reload(true);
               //document.location.href='/Pedido/listar/';
          }
      });

  }
