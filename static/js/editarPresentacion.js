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
