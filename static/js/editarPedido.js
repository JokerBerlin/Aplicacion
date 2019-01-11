$(document).ready(function() {
  //$('#id_Total').text("0.00");
  $("#generarAlmacen").click(function() {
    var num=1;
    productos = [];
    contador = 0;
    $('#tabla tbody tr').each(function (index) {
      // productosPedido = [];
      // var id = $(this).find("td").eq(0).html();
      // var cantidad = $(this).find("td").eq(1).html();
      // console.log(codigo);
      $(this).children("td").each(function (index2) {
          producto = [];
          //dato = index;
          console.log(index);
          switch (index2) {
              case 0:
                  id = $(this).text();
              case 2:
                  cantidad = $("#cantidad"+index ).val();
                  //
                  // if (cantidad.indexOf(',')==true) {
                  //   cantidad=cantidad.replace(",",".");
                  // }

                  break;
          }

      });
      contador = 1;
      productos.push([id,cantidad]);
      });
      console.log(productos);
      if (contador == 1) {
          var pedido = document.getElementById("pedido_id").value;
          console.log(pedido);
          var datos = {productos: productos,pedido:pedido};
          var sendData = JSON.stringify(datos);
          $.ajax({
              type: "POST",
              dataType: "json",
              url: "/Pedido/modificar/",
              data: sendData,
              contentType: "application/json; charset=utf-8",
              async: false,
              cache: false,
              CrossDomain: true,

              success: function (result) {
              //     var id_venta = result["id_venta"];
                   alert('Pedido modificado');
                   //location.reload(true);
                   document.location.href='/Pedido/listar/1/';
              }
          });
      }else{
          alert("No registró ningún producto");
      }
  });



});

function eventoCambio(valor){
    var cantidad = $('#cantidad'+valor+'').val();
    console.log(cantidad);
    if (cantidad != ''){
        var precioU = $('#precioUnitario'+valor+'').text();
        console.log(cantidad);
        console.log(precioU);
        var subTot = parseFloat(cantidad) * parseFloat(precioU);
        $('#SubTotal'+valor+'').text(subTot.toFixed(2));
        RefrescarTotal();
    }else{
        alert("Ingrese una cantidad válida");
        $('#cantidad'+valor+'').focus();
    }

}

function RefrescarTotal(){
    Total=0;
    $('#tabla tbody tr').each(function(){
        valor = $(this).find('td').eq(8)[0].innerText;
        //console.log(valor);
        Total = Total + parseFloat(valor);
        $('#id_Total').text(Total.toFixed(2));
        //alert(Total);
    });
}
