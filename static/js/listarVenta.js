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
  });
});

//datepicker
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
  $( "#desde" ).datepicker();
  $( "#hasta" ).datepicker();
} );

$( function() {
  $( "#desde" ).datepicker();
} );

$( function() {
  $( "#hasta" ).datepicker();
} );

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
