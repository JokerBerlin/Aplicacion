function seleccionarTipo(){
    console.log(document.getElementById('cmbTipoOperacion').value);
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/Caja/buscar-detalle/",
        data: {

            'tipoOperacion': document.getElementById('cmbTipoOperacion').value,
        },
        async: false,
        success: function(data) {
            console.log(data);
            var cmbOperacion = document.getElementById('cmbOperacion');
            if (data.detalle == ''){
                cmboOperacion.value = '';
            } else {
              cmbOperacion.options.length=0;
              for (var i = 0; i < data.length; i+=1) {
                  var option = document.createElement('option');
                  option.value = data[i].id;
                  option.text = data[i].nombre;
                  cmbOperacion.appendChild(option);
              }
            }
        },

    });
}
