$(document).ready(function() {
  $('#id_Total').text("0.00");
  window.onload = function(){
    $("#cmbRecibo").focus();
    var Total = 0;
    $("#tabla tbody tr").each(function (index) {

        $(this).children("td").each(function (index2) {

            //dato = index;
            console.log(index);
            switch (index2) {
                case 6:
                    valor = $(this).text();
                    Total = Total + parseFloat(valor);

                    break;
            }

        });
        console.log(Total);
        contador = 1;

    });
    $('#id_Total').text(Total);
  }

  $("#generarAlmacen").click(function() {
    var num=1;
    productos = [];
    contador = 0;
    var pedido = document.getElementById("pedido_id").value;
    var cliente = document.getElementById("inpt-cliente").value;
    var total = document.getElementById("id_Total").innerHTML;
    var tipoRecibo = document.getElementById("cmbRecibo").value;
    var numeroRecibo = document.getElementById("nroRecibo").value;

    var datos = {cliente:cliente,total:total,tipoRecibo:tipoRecibo,numeroRecibo:numeroRecibo};
    var sendData = JSON.stringify(datos);
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/Pedido/venta/"+pedido+"/",
        data: sendData,
        contentType: "application/json; charset=utf-8",
        async: false,
        cache: false,
        CrossDomain: true,
        success: function (result) {
        //     var id_venta = result["id_venta"];
            console.log(pedido);
             alert('Venta registrada');
             //location.reload(true);
             document.location.href='/imprimir/'+pedido+'/';
             timeoutID = window.setTimeout('listarVenta();', 3000);

        }
    });
  });
});


function listarVenta(){
    document.location.href='/Venta/listar/';
}
