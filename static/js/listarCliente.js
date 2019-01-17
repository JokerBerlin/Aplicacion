$(document).ready(function(){
  $( "#inpt-cliente" ).focus();
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
								document.forms.form_busca.action =  "/Cliente/detalle/"+item.id+"/" ;
                if( isNaN(valorCliente) ){
                    return {label: item.nombre,
														idcliente: item.id};

                }else{
                    return {label: item.numerodocumento,
											idcliente:item.id};

                }


								$(document).on('ready',function(){
						    $('#btn-buscar').submit(function(){
						        var url = "/Cliente/detalle/"+item.id+"/";
						        $.ajax({
						           type: "POST",
						           url: url,
						           data: $("#form_busca").serialize(),
						           success: function(data)
						           {
						             $('#resp').html(data);
						           }
						       });
						    });
						});

              }));
              }
          });
      },
      minLength: 2,
			select: function (event, ui) {
          document.location.href="/Cliente/detalle/"+ui.item.idcliente+"/";
      }
  });


});

function eliminarIdentificador(identificadorId) {
		var request = $.ajax({
				type: "POST",
				url: "{% url 'eliminar_cliente' %}",
				data: {
						"csrfmiddlewaretoken": "{{ csrf_token }}",
						"identificador_id": identificadorId
				},
		});
		request.done(function(response) {
				alert("El cliente fue desactivado con exito");
				$('#myModal').modal('toggle');
				location.reload(true);
				//$("#tabla" + identificadorId).remove();
		});
};
	selPersona = function(idPersona, nombre){
		document.getElementById('nombreCliente').innerHTML = nombre;
		$("#eliminar").attr("onclick","eliminarIdentificador('"+idPersona+"')");
	};
