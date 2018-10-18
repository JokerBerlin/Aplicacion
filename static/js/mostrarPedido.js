$(document).ready(function() {
  $('#id_Total').text("0.00");
  window.onload = function(){
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
    var nroRecibo = document.getElementById("nroRecibo").value;
    var datos = {cliente:cliente,total:total,nroRecibo:nroRecibo};
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
             alert('Venta registrada');
             //location.reload(true);
             document.location.href='/Venta/listar/';
        }
    });
  });
});
