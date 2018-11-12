$(document).ready(function(){
  $('#bt_add').click(function(){
    //nombre de presentacion
    //cantidad presentacion
    presentaciones = [];
    var combo = document.getElementById("cmbPresentacion");
    var presentacion = combo.options[combo.selectedIndex].text;
    var cantidadPrincipal = $('#cantPresentacion').val();
    var precio1 = $('#1Precio').val();
    var precio2 = $('#2Precio').val();
    var precio3 = $('#3Precio').val();
    presentaciones.push([presentacion,cantidadPrincipal,precio1,precio2,precio3]);
    console.log(presentaciones);
    var producto = document.getElementById("id_nombre").value;
    var productoId = document.getElementById("productoId").value;

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
             document.location.href='/Producto/editar/'+productoId+'/';
        }
    });
  });


});
function EliminarPresentacionProducto(presentacion,productoId, presentacionId){
    console.log(presentacion);
    document.getElementById('nombrePresentacion').innerHTML = presentacion;
    $("#eliminarPresentacionProd").attr("href","/Presentacion/eliminar/"+presentacionId+"/"+productoId+"/");
}

function EditarProducto(){
  $('#actualizarProducto').text('Guardar');
  $('#actualizarProducto').prop('class', 'btn btn-primary');

  $('#id_nombre').prop('disabled', false);
  temp=$("#id_nombre").val();
  $("#id_nombre").val('');
  $("#id_nombre").val(temp);
  $("#id_nombre").focus();
  //var foco = $('#id_nombre').val().length;
  // $('#id_nombre').keyup(function(e){
  //         if($(this).val().length==$(this).attr('maxlength'))
  //             $(this).next(':input').focus()
  //     })
  // }
  var val = $('#id_nombre').val();
  val.focus();
  //$("#id_nombre").val($("#id_nombre").val());
  $('#id_codigo').prop('disabled', false);
  $('#id_imagen').prop('disabled', false);
  $('#id_url').prop('disabled', false);

}

function EditarPresentacionProducto(precio1Id,precio2Id,precio3Id,productoPresentacionId,contador){
  $('#editar'+contador+'').text('Actualizar');
  $('#valorPrecio'+contador+'').prop('disabled', false);
  $('#valorPrecio'+contador+'').focus();
  $('#Precio1'+contador+'').prop('disabled', false);
  $('#Precio2'+contador+'').prop('disabled', false);
  $('#Precio3'+contador+'').prop('disabled', false);
  $('#editar'+contador+'').attr("onclick","");
  //$('#editar'+contador+'').attr("href","/Producto/listar/");
  console.log(precio1Id+','+precio2Id+','+precio3Id+','+productoPresentacionId);
  $('#editar'+contador+'').click(function(){
    var tipo = $('#editar'+contador+'').text();
    if (tipo == 'Actualizar'){
      var productoId = $('#productoId').val();
      var valorPrecio = $('#valorPrecio'+contador+'').val();
      var precio1 = $('#Precio1'+contador+'').val();
      var precio2 = $('#Precio2'+contador+'').val();
      var precio3 = $('#Precio3'+contador+'').val();

      var datos = {productoPresentacionId:productoPresentacionId,valorPrecio:valorPrecio, precio1Id:precio1Id,precio1:precio1,precio2Id:precio2Id,precio2:precio2,precio3Id:precio3Id,precio3:precio3};
      console.log(datos);
      var sendData = JSON.stringify(datos);

      $.ajax({
          type: "POST",
          dataType: "json",
          url: "/Presentacion/editar/",
          data: sendData,
          contentType: "application/json; charset=utf-8",
          async: false,
          cache: false,
          CrossDomain: true,

          success: function (result) {
          //     svar id_venta = result["id_venta"];
               alert('Pedido modificado');
               //location.reload(true);
               document.location.href='/Producto/editar/'+productoId+'/';
          }
      });
    }
  });
}
