function eliminarIdentificador(identificadorId) {
		var request = $.ajax({
				type: "POST",
				url: "/Lote/eliminar/",
				data: {
						"csrfmiddlewaretoken": "{{ csrf_token }}",
						"identificador_id": identificadorId
				},
		});
		request.done(function(response) {
        if(response['error']=='error'){
            alert("El lote no se puede eliminar");
            $('#myModal').modal('toggle');
        }else{
            alert("El lote fue eliminado con exito");
            $('#myModal').modal('toggle');
            document.location.href='/Lote/listar/';
        }

		});
};

selLote = function(idLote, fecha){
		document.getElementById('fechaLote').innerHTML = fecha.toString();
		$("#eliminar").attr("onclick","eliminarIdentificador('"+idLote+"')");
};
