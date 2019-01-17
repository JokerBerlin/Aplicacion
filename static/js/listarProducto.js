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
                  document.forms.form_busca.action =  "/Producto/detalle/"+item.id+"/";
                  var idValor = item.id;
                  return {label:item.nombre,
                        idproducto: item.id};

              }));


              }
          });
      },
      minLength: 2,
      select: function (event, ui) {
          document.location.href='/Producto/detalle/'+ui.item.idproducto+"/";
      }
  });
});

function imprimirProducto(){
  var objeto=document.getElementById('imprimirProductos');  //obtenemos el objeto a imprimir
  var ventana=window.open('','_blank');  //abrimos una ventana vacía nueva
  ventana.document.write(objeto.innerHTML);  //imprimimos el HTML del objeto en la nueva ventana
  ventana.document.close();  //cerramos el documento
  ventana.print();  //imprimimos la ventana
  ventana.close();  //cerramos la ventana
}

function eliminarIdentificador(identificadorId) {
		var request = $.ajax({
				type: "POST",
				url: "{% url 'eliminar_producto' %}",
				data: {
						"csrfmiddlewaretoken": "{{ csrf_token }}",
						"identificador_id": identificadorId
				},
		});
		request.done(function(response) {
				alert("El producto fue desactivado con exito");
				$('#myModal').modal('toggle');
				$("#tabla" + identificadorId).remove();
		});
};
selProducto = function(idProducto, nombre){
		document.getElementById('nombreProducto').innerHTML = nombre;
		$("#eliminar").attr("onclick","eliminarIdentificador('"+idProducto+"')");
};
