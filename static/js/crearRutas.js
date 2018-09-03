$(document).ready(function(){
        $('#bt_add').click(function(){
            agregar();
        });
        $('#bt_del').click(function(){
            eliminar(id_fila_selected);
        });

        $('#bt_delall').click(function(){
            eliminarTodasFilas();
        });
    });

    function reset_values(){
        $('#id_cliente').val('');
        $('#direccion').val('');
    }

    var cont=0;
    var id_fila_selected=[];
    function agregar(){
        cont++;
        Cliente = $('#id_cliente').val();
        direccion = $('#direccion').val();
        error = "";
        if (Cliente==''){
            error = 1;
        }

        if (error=="") {
            var fila=
            '<tr class="selected" id="fila'+cont+'" onclick="seleccionar(this.id);"><td>'+cont+'</td><td>'+Cliente+'</td><td>'+direccion+'</td></tr>';
            $('#tabla').append(fila);

            reset_values();
            reordenar();
        }
        else{
            switch(error) {
            case 1:
                alert("Seleccione un cliente válido!");
                $( "#id_cliente" ).focus();
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
        ValorRestar = 0;
        for(var i=0; i<id_fila.length; i++){
            $('#'+id_fila[i]).children("td").each(function (index2) {
                switch (index2) {
                    case 5:
                        ValorRestar = parseFloat($(this).text()).toFixed(2);
                        break;
                }
            });

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
